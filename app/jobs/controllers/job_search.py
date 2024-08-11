import logging
from datetime import datetime
import hashlib

from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.core.cache import cache

from jobs.models import JobPosting

logger = logging.getLogger(__name__)
JOBS_PER_PAGE = 20


class JobSearch:
    def __init__(self, request):
        self.request = request
        self.params = request.GET.dict()
        self.jobs = (JobPosting.objects.select_related('company').
                     filter(status=JobPosting.Status.PUBLISHED).order_by("published"))

    def get_cache_key(self):
        sorted_params = sorted(self.params.items())
        params_string = str(sorted_params)
        hash_key = hashlib.md5(params_string.encode()).hexdigest()
        return f"jobs_search_{hash_key}"

    def get_cached_results(self):
        cache_key = self.get_cache_key()
        return cache.get(cache_key)

    def cache_results(self, results):
        cache_key = self.get_cache_key()
        cache.set(cache_key, results, timeout=600)

    def apply_text_search(self):
        text = self.params.get("text")
        search_all = self.params.get("search_all")

        if text:
            if search_all == "true":
                self.jobs = self.jobs.filter(
                    Q(position__icontains=text) |
                    Q(long_description__icontains=text) |
                    Q(primary_keyword__icontains=text) |
                    Q(secondary_keyword__icontains=text) |
                    Q(extra_keywords__icontains=text)
                ).order_by('published')
            else:
                query = SearchQuery(text)
                self.jobs = self.jobs.annotate(
                    rank=SearchRank('search_vector', query)
                ).filter(search_vector=query).order_by('-rank')

    def apply_date_filters(self):
        start_date = self.params.get("start_date")
        end_date = self.params.get("end_date")

        if start_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            self.jobs = self.jobs.filter(published__gte=start_date)
        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            self.jobs = self.jobs.filter(published__lte=end_date)

    def apply_company_filter(self):
        company_name = self.params.get("company_name")
        if company_name:
            self.jobs = self.jobs.filter(company__name__icontains=company_name)

    def apply_salary_filter(self):
        min_salary = self.params.get("min_salary")
        if min_salary:
            self.jobs = self.jobs.filter(salary_max__gte=min_salary)

    def apply_remote_type_filter(self):
        remote_types = self.params.get("remote_types", "").split(',')
        if remote_types and remote_types != ['']:
            self.jobs = self.jobs.filter(remote_type__in=remote_types)

    def apply_location_filters(self):
        countries = self.params.get("countries", "").split(',')
        cities = self.params.get("cities", "").split(',')

        if countries and countries != ['']:
            country_filter = Q()
            for country in countries:
                if country == 'OTHER':
                    country_filter |= ~Q(country__in=['UKR', 'POL', 'USA'])
                else:
                    country_filter |= Q(country__contains=country)
            self.jobs = self.jobs.filter(country_filter).distinct()

        if cities and cities != ['']:
            city_filter = Q()
            for city in cities:
                if city == 'OTHER':
                    city_filter |= ~Q(location__in=['Киев', 'Львов', 'Харьков'])
                else:
                    city_filter |= Q(location__contains=city)
            self.jobs = self.jobs.filter(city_filter)

    def apply_english_level_filter(self):
        english_levels = self.params.get("english_levels", "").split(',')
        if english_levels and english_levels != ['']:
            if 'no_english' in english_levels:
                self.jobs = self.jobs.filter(Q(english_level__in=english_levels) | Q(english_level__isnull=True))
            else:
                self.jobs = self.jobs.filter(english_level__in=english_levels)

    def apply_experience_filter(self):
        experience_years = self.params.get("experience_years", "").split(',')
        if experience_years and experience_years != ['']:
            experience_filter = Q()
            for exp in experience_years:
                if exp == '5+':
                    experience_filter |= Q(experience_years__gte=5)
                else:
                    experience_filter |= Q(experience_years=exp)
            self.jobs = self.jobs.filter(experience_filter)

    def apply_all_filters(self):
        logger.debug("Applying all filters")
        self.apply_text_search()
        self.apply_date_filters()
        self.apply_company_filter()
        self.apply_salary_filter()
        self.apply_remote_type_filter()
        self.apply_location_filters()
        self.apply_english_level_filter()
        self.apply_experience_filter()

    def get_results(self):
        logger.debug("Entering get_results")
        cached_results = self.get_cached_results()
        if cached_results:
            logger.info("Jobs list page requested from cache")
            return cached_results

        self.apply_all_filters()
        jobs_count = self.jobs.count()
        paginator = Paginator(self.jobs, JOBS_PER_PAGE)
        page = int(self.request.GET.get("page", 1))
        jobs_list = paginator.page(page)
        has_next = page < paginator.num_pages

        results = (jobs_list, jobs_count, has_next)
        self.cache_results(results)
        return results
