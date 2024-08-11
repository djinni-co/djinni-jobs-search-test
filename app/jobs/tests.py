import json
import pytest

from django.test import RequestFactory
from django.http import JsonResponse, HttpResponse
from django.core.cache import cache

from jobs.models import JobPosting, Company
from jobs.controllers.job_search import JobSearch
from jobs.views import all_job_list


@pytest.fixture
def job_search_setup():
    company = Company.objects.create(name="Test Company")
    JobPosting.objects.create(
        position="Software Developer",
        company=company,
        status=JobPosting.Status.PUBLISHED,
        salary_max=1000,
        remote_type="office",
        country="USA",
        location="Харьков",
        english_level="fluent",
        experience_years=3
    )
    JobPosting.objects.create(
        position="Data Scientist",
        company=company,
        status=JobPosting.Status.PUBLISHED,
        salary_max=4000,
        remote_type="full_remote",
        country="UKR",
        location="Киев",
        english_level="pre",
        experience_years=5
    )


@pytest.mark.django_db
class TestJobSearch:
    def test_text_search(self, job_search_setup):
        factory = RequestFactory()
        request = factory.get('/?text=Software')
        job_search = JobSearch(request)
        job_search.apply_text_search()
        assert job_search.jobs.count() == 1
        assert job_search.jobs.first().position == "Software Developer"

    def test_salary_filter(self, job_search_setup):
        factory = RequestFactory()
        request = factory.get('/?min_salary=3000')
        job_search = JobSearch(request)
        job_search.apply_salary_filter()
        assert job_search.jobs.count() == 1
        assert job_search.jobs.first().position == "Data Scientist"

    def test_remote_type_filter(self, job_search_setup):
        factory = RequestFactory()
        request = factory.get('/?remote_types=office')
        job_search = JobSearch(request)
        job_search.apply_remote_type_filter()
        assert job_search.jobs.count() == 1
        assert job_search.jobs.first().position == "Software Developer"

    def test_location_filters(self, job_search_setup):
        factory = RequestFactory()
        request = factory.get('/?countries=UKR&cities=Киев')
        job_search = JobSearch(request)
        job_search.apply_location_filters()
        assert job_search.jobs.count() == 1
        assert job_search.jobs.first().position == "Data Scientist"

    def test_english_level_filter(self, job_search_setup):
        factory = RequestFactory()
        request = factory.get('/?english_levels=fluent')
        job_search = JobSearch(request)
        job_search.apply_english_level_filter()
        assert job_search.jobs.count() == 1
        assert job_search.jobs.first().position == "Software Developer"

    def test_experience_filter(self, job_search_setup):
        factory = RequestFactory()
        request = factory.get('/?experience_years=5')
        job_search = JobSearch(request)
        job_search.apply_experience_filter()
        assert job_search.jobs.count() == 1
        assert job_search.jobs.first().position == "Data Scientist"

    def test_caching(self, job_search_setup):
        factory = RequestFactory()
        request = factory.get('/')
        job_search = JobSearch(request)
        cache.clear()
        assert job_search.get_cached_results() is None
        results = job_search.get_results()
        cached_results = job_search.get_cached_results()

        assert isinstance(cached_results, tuple)
        assert len(cached_results) == 3
        assert isinstance(cached_results[0], type(results[0]))
        assert cached_results[1] == results[1]
        assert cached_results[2] == results[2]

        assert list(cached_results[0]) == list(results[0])


@pytest.mark.django_db
class TestAllJobList:
    def test_all_job_list_ajax(self, job_search_setup):
        factory = RequestFactory()
        request = factory.get('/')
        request.is_ajax = lambda: True
        response = all_job_list(request)
        assert isinstance(response, JsonResponse)
        data = json.loads(response.content.decode('utf-8'))
        assert 'jobs' in data
        assert 'jobs_count' in data
        assert 'has_next' in data

    def test_all_job_list_non_ajax(self, job_search_setup):
        factory = RequestFactory()
        request = factory.get('/')
        request.is_ajax = lambda: False
        response = all_job_list(request)
        assert isinstance(response, HttpResponse)
        assert response.status_code == 200
        assert 'text/html' in response['Content-Type']
