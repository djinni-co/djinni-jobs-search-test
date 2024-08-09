from django.db import models

from .enums import AcceptRegion
from .enums import CompanyType
from .enums import EnglishLevel
from .enums import JobDomain
from .enums import RemoteType
from .enums import Status


class JobPosting(models.Model):
    # Job description fields
    position = models.CharField(max_length=250, blank=False, default='')
    primary_keyword = models.CharField(max_length=50, blank=True, default='', null=True)
    secondary_keyword = models.CharField(max_length=50, blank=True, default='', null=True)
    long_description = models.TextField(blank=True, default='')

    domain = models.CharField(
        max_length=20,
        blank=True,
        default='',
        null=True,
        choices=JobDomain.choices,
    )
    company_type = models.CharField(
        max_length=20,
        blank=True,
        default='',
        null=True,
        choices=CompanyType.choices,
    )

    salary_min = models.IntegerField(blank=True, null=True, default=0)
    salary_max = models.IntegerField(blank=True, null=True, default=0)
    public_salary_min = models.IntegerField(blank=True, null=True, default=0)
    public_salary_max = models.IntegerField(blank=True, null=True, default=0)

    # Skills
    extra_keywords = models.CharField(max_length=250, blank=True, null=True, default='')
    experience_years = models.FloatField(default=0)
    english_level = models.CharField(
        max_length=15,
        blank=True,
        default='',
        null=True,
        choices=EnglishLevel.choices,
    )

    country = models.CharField(max_length=250, blank=True, default='', null=True)
    location = models.CharField(max_length=250, blank=True, default='', null=True)
    accept_region = models.CharField(
        max_length=20,
        blank=True,
        default='',
        null=True,
        choices=AcceptRegion.choices,
    )
    remote_type = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default='',
        choices=RemoteType.choices,
    )

    is_parttime = models.BooleanField(default=False, db_index=True)
    has_test = models.BooleanField(default=False, db_index=True)
    requires_cover_letter = models.BooleanField(default=False, db_index=True)
    is_ukraine_only = models.BooleanField(default=False, db_index=True)
    is_reserving_from_mobilisation = models.BooleanField(default=False)

    # Counts
    unread_count = models.IntegerField(blank=False, default=0)
    search_count = models.IntegerField(blank=False, default=0)  # unused, how many candidates for this job
    views_count = models.IntegerField(blank=False, default=0)
    applications_count = models.IntegerField(blank=False, default=0)
    sent_count = models.IntegerField(blank=False, default=0)

    recruiter = models.ForeignKey('Recruiter', on_delete=models.CASCADE, blank=True, null=True, db_index=True)
    company = models.ForeignKey(
        'Company',
        models.SET_NULL,
        blank=True,
        null=True,
        db_index=True,
    )

    # Meta fields
    status = models.CharField(
        blank=True,
        default=Status.DRAFT,
        db_index=True,
        choices=Status.choices,
        max_length=10,
    )
    last_modified = models.DateTimeField(blank=True, null=True, auto_now=True, db_index=True)
    published = models.DateTimeField(blank=True, null=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)


class Recruiter(models.Model):
    email = models.EmailField(blank=False, db_index=True, unique=True)
    name = models.CharField(max_length=250, blank=False, default='')
    company_id = models.IntegerField(blank=True, null=True)
    slug = models.SlugField()


class Company(models.Model):
    name = models.CharField(max_length=250, blank=False, default='')
    company_type = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default='',
        choices=CompanyType.choices,
    )
    country_code = models.CharField(
        max_length=3,
        blank=True, null=True,
        default='',
        db_index=True,
    )
    is_international = models.BooleanField(default=False)
    dou_link = models.CharField(max_length=255, blank=True, null=True, default='')
    shortcode = models.CharField(
        max_length=10,
        db_index=True,
        blank=False,
        default='',
        unique=True,
    )
    logo_url = models.CharField(max_length=255, blank=True, null=True, default='')
    created = models.DateTimeField(auto_now_add=True, db_index=True)
