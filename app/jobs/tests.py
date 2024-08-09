from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from .factories import CompanyFactory
from .factories import JobPostingFactory
from .factories import RecruiterFactory


class JobPostingTestCase(APITestCase):
    client: APIClient
    maxDiff = None

    def setUp(self):
        self.client = APIClient()
        self.company1 = CompanyFactory(name='Example Corp', shortcode='excorp')
        self.company2 = CompanyFactory(name='Tech Solutions', shortcode='techsol')
        self.company3 = CompanyFactory(name='Global Tech', shortcode='glotech')

        self.recruiter1 = RecruiterFactory(company_id=self.company1.id)
        self.recruiter2 = RecruiterFactory(company_id=self.company2.id)
        self.recruiter3 = RecruiterFactory(company_id=self.company3.id)

        self.job1 = JobPostingFactory(
            position='Software Engineer',
            long_description='A job for a software engineer',
            primary_keyword='Python',
            secondary_keyword='Django',
            extra_keywords='API, Backend',
            salary_min=60000,
            salary_max=90000,
            remote_type='office',
            location='New York',
            english_level='fluent',
            experience_years=3,
            company=self.company1,
            recruiter=self.recruiter1,
            domain='Fintech',
            company_type='Product',
            applications_count=100,
            published=timezone.now() - timezone.timedelta(days=10),
        )
        self.job2 = JobPostingFactory(
            position='Data Scientist',
            long_description='A job for a data scientist with Python skills',
            primary_keyword='Python',
            secondary_keyword='Machine Learning',
            extra_keywords='Data Analysis, AI',
            salary_min=70000,
            salary_max=100000,
            remote_type='partly_remote',
            location='San Francisco',
            english_level='intermediate',
            experience_years=5,
            company=self.company2,
            recruiter=self.recruiter2,
            domain='Healthcare',
            company_type='Outsource',
            applications_count=50,
            published=timezone.now() - timezone.timedelta(days=20),
        )
        self.job3 = JobPostingFactory(
            position='Blockchain Developer',
            long_description='A job for a blockchain developer with Solidity skills',
            primary_keyword='Solidity',
            secondary_keyword='Blockchain',
            extra_keywords='Ethereum, Smart Contracts',
            salary_min=80000,
            salary_max=120000,
            remote_type='full_remote',
            location='London',
            english_level='fluent',
            experience_years=4,
            company=self.company3,
            recruiter=self.recruiter3,
            domain='Crypto',
            company_type='Product',
            applications_count=150,
            published=timezone.now() - timezone.timedelta(days=5),
        )
        self.job4 = JobPostingFactory(
            position='Fullstack Developer',
            long_description='A job for a fullstack developer',
            primary_keyword='JavaScript',
            secondary_keyword='React',
            extra_keywords='Frontend, Backend',
            salary_min=50000,
            salary_max=80000,
            remote_type='candidate_choice',
            location='Berlin',
            english_level='advanced',
            experience_years=2,
            company=self.company1,
            recruiter=self.recruiter1,
            domain='E-commerce',
            company_type='Product',
            applications_count=75,
            published=timezone.now() - timezone.timedelta(days=15),
        )
        self.job5 = JobPostingFactory(
            position='DevOps Engineer',
            long_description='A job for a DevOps engineer',
            primary_keyword='AWS',
            secondary_keyword='Kubernetes',
            extra_keywords='Cloud, Infrastructure',
            salary_min=90000,
            salary_max=130000,
            remote_type='candidate_choice',
            location='Tokyo',
            english_level='advanced',
            experience_years=6,
            company=self.company2,
            recruiter=self.recruiter2,
            domain='Cloud',
            company_type='Outsource',
            applications_count=80,
            published=timezone.now() - timezone.timedelta(days=7),
        )

    def test_exclude_search_terms(self):
        url = reverse('jobposting-list') + '?include_terms=Python&exclude_terms=Data'
        response = self.client.get(url, format='json')
        print("Exclude Search Terms Response:", response.json())

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.json()['results']), 1)

    def test_search_by_company_name(self):
        url = reverse('jobposting-list') + '?search=Example Corp'
        response = self.client.get(url, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.json()['results']), 2)

        url = reverse('jobposting-list') + '?search=Solutions'
        response = self.client.get(url, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.json()['results']), 2)

    def test_search_by_experience_years(self):
        url = reverse('jobposting-list') + '?experience_years=6'
        response = self.client.get(url, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.json()['results']), 1)

        url = reverse('jobposting-list') + '?experience_years=4'
        response = self.client.get(url, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.json()['results']), 3)

    def test_search_by_remote_type(self):
        url = reverse('jobposting-list') + '?remote_type=office'
        response = self.client.get(url, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.json()['results']), 1)

    def test_search_by_salary(self):
        url = reverse('jobposting-list') + '?salary_min=60000&salary_max=90000'
        response = self.client.get(url, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.json()['results']), 1)

    def test_search_by_position_and_description(self):
        url = reverse('jobposting-list') + '?search=Software Engineer'
        response = self.client.get(url, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.json()['results']), 1)

        url = reverse('jobposting-list') + '?search=blockchain developer'
        response = self.client.get(url, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.json()['results']), 1)

    def test_search_by_keywords(self):
        url = reverse('jobposting-list') + '?search=Python'
        response = self.client.get(url, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.json()['results']), 2)

    def test_search_by_location(self):
        url = reverse('jobposting-list') + '?search=Tokyo'
        response = self.client.get(url, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.json()['results']), 1)

    def test_search_by_english_level(self):
        url = reverse('jobposting-list') + '?english_level=fluent'
        response = self.client.get(url, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.json()['results']), 2)

        url = reverse('jobposting-list') + '?english_level=intermediate'
        response = self.client.get(url, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.json()['results']), 1)

    def test_search_by_company_type(self):
        url = reverse('jobposting-list') + '?company_type=Outsource'
        response = self.client.get(url, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.json()['results']), 2)

    def test_search_by_domain(self):
        url = reverse('jobposting-list') + '?domain=Fintech'
        response = self.client.get(url, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.json()['results']), 1)

        url = reverse('jobposting-list') + '?domain=Crypto'
        response = self.client.get(url, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.json()['results']), 1)
