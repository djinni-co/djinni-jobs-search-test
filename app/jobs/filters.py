from django_filters import CharFilter
from django_filters import NumberFilter
from django_filters import rest_framework as filters

from .models import JobPosting


class JobPostingFilterSet(filters.FilterSet):
    salary_min = NumberFilter(field_name='salary_min', lookup_expr='gte')
    salary_max = NumberFilter(field_name='salary_max', lookup_expr='lte')
    experience_years = NumberFilter(field_name='experience_years', lookup_expr='gte')
    domain = CharFilter(field_name='domain', lookup_expr='exact')
    company_type = CharFilter(field_name='company_type', lookup_expr='exact')

    class Meta:
        model = JobPosting
        fields = [
            'remote_type',
            'country',
            'location',
            'english_level',
            'company',
            'domain',
            'company_type',
            'salary_min',
            'salary_max',
            'experience_years',
        ]
