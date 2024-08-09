import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from .enums import CompanyType
from .enums import EnglishLevel
from .enums import JobDomain
from .enums import RemoteType
from .enums import Status
from .models import Company
from .models import JobPosting
from .models import Recruiter


class CompanyFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: f'Company {n}')
    company_type = factory.Iterator([choice[0] for choice in CompanyType.choices])
    country_code = factory.Faker('country_code')
    is_international = factory.Faker('boolean')
    dou_link = factory.Faker('url')
    shortcode = factory.Sequence(lambda n: f'sc{n:03d}')
    logo_url = factory.Faker('url')
    created = factory.Faker('date_time', tzinfo=timezone.utc)

    class Meta:
        model = Company


class RecruiterFactory(DjangoModelFactory):
    email = factory.Faker('email')
    name = factory.Faker('name')
    company_id = factory.Faker('random_int', min=1, max=100)
    slug = factory.Faker('slug')

    class Meta:
        model = Recruiter


class JobPostingFactory(DjangoModelFactory):
    position = factory.Sequence(lambda n: f'Position {n}')
    primary_keyword = factory.Faker('word')
    secondary_keyword = factory.Faker('word')
    long_description = factory.Faker('paragraph')
    domain = factory.Iterator([choice[0] for choice in JobDomain.choices])
    company_type = factory.Iterator([choice[0] for choice in CompanyType.choices])
    salary_min = factory.Faker('random_int', min=50000, max=80000)
    salary_max = factory.Faker('random_int', min=90000, max=130000)
    public_salary_min = factory.Faker('random_int', min=50000, max=80000)
    public_salary_max = factory.Faker('random_int', min=90000, max=130000)
    extra_keywords = factory.Faker('words', nb=3, ext_word_list=None)
    english_level = factory.Iterator([choice[0] for choice in EnglishLevel.choices])
    country = factory.Faker('country')
    location = factory.Faker('city')
    accept_region = factory.Iterator([choice[0] for choice in RemoteType.choices])
    remote_type = factory.Iterator([choice[0] for choice in RemoteType.choices])
    is_parttime = factory.Faker('boolean')
    has_test = factory.Faker('boolean')
    requires_cover_letter = factory.Faker('boolean')
    is_ukraine_only = factory.Faker('boolean')
    is_reserving_from_mobilisation = factory.Faker('boolean')
    unread_count = factory.Faker('random_int', min=0, max=100)
    search_count = factory.Faker('random_int', min=0, max=100)
    views_count = factory.Faker('random_int', min=0, max=100)
    applications_count = factory.Faker('random_int', min=0, max=100)
    sent_count = factory.Faker('random_int', min=0, max=100)
    recruiter = factory.SubFactory(RecruiterFactory)
    company = factory.SubFactory(CompanyFactory)
    status = factory.Iterator([choice[0] for choice in Status.choices])
    last_modified = factory.Faker('date_time', tzinfo=timezone.utc)
    published = factory.Faker('date_time', tzinfo=timezone.utc)
    created = factory.Faker('date_time', tzinfo=timezone.utc)

    class Meta:
        model = JobPosting
