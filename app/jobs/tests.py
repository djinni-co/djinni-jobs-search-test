from django.test import TestCase
from django.urls import reverse
from .models import JobPosting, Company


class JobPostingModelTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            name="Test Company", company_type="product", country_code="USA"
        )
        self.job = JobPosting.objects.create(
            position="Python Developer",
            primary_keyword="Python",
            secondary_keyword="Django",
            extra_keywords="REST API",
            long_description="Looking for an experienced Python Developer",
            company=self.company,
            salary_max=100000,
            remote_type="full_remote",
            english_level="intermediate",
            experience_years=3,
        )

    def test_job_posting_creation(self):
        """Test that a JobPosting instance is created successfully"""
        self.assertEqual(self.job.position, "Python Developer")
        self.assertEqual(self.job.company.name, "Test Company")
        self.assertEqual(self.job.salary_max, 100000)


class JobPostingFilterTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            name="Test Company", company_type="product", country_code="USA"
        )
        self.job1 = JobPosting.objects.create(
            position="Python Developer",
            primary_keyword="Python",
            company=self.company,
            salary_max=100000,
        )
        self.job2 = JobPosting.objects.create(
            position="Java Developer",
            primary_keyword="Java",
            company=self.company,
            salary_max=90000,
        )

    def test_filter_by_primary_keyword(self):
        """Test that filtering by primary keyword returns the correct job"""
        response = self.client.get(
            reverse("jobs_list"), {"keyword_search": "Python"}
            )
        self.assertContains(response, self.job1.position)
        self.assertNotContains(response, self.job2.position)

    def test_filter_by_salary(self):
        """Test that filtering by salary returns the correct jobs"""
        response = self.client.get(reverse("jobs_list"), {"salary_max": 95000})
        self.assertContains(response, self.job2.position)
        self.assertNotContains(response, self.job1.position)


class JobPostingViewTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            name="Test Company", company_type="product", country_code="USA"
        )
        self.job = JobPosting.objects.create(
            position="Python Developer",
            primary_keyword="Python",
            company=self.company,
            salary_max=100000,
        )

    def test_jobs_list_view(self):
        """Test that the jobs list view returns the correct jobs"""
        response = self.client.get(reverse("jobs_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.job.position)
