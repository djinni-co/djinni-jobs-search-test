import django_filters
from django import forms

from jobs.utils import get_unique_choices, get_choices
from jobs.models import (
    JobPosting, 
    JobDomain, 
    CompanyType, 
    EnglishLevel, 
    AcceptRegion, 
    RemoteType
)

class JobPostingFilter(django_filters.FilterSet):
    """ Filters for job postings. """
    position = django_filters.ChoiceFilter(choices=get_unique_choices('position', JobPosting))
    domain = django_filters.MultipleChoiceFilter(
        choices=JobDomain.choices,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    company_type = django_filters.MultipleChoiceFilter(
        choices=CompanyType.choices,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    experience_years = django_filters.MultipleChoiceFilter(
        choices=get_unique_choices('experience_years', JobPosting),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    english_level = django_filters.MultipleChoiceFilter(
        choices=EnglishLevel.choices,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    accept_region = django_filters.MultipleChoiceFilter(
        choices=AcceptRegion.choices,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    remote_type = django_filters.MultipleChoiceFilter(
        choices=RemoteType.choices,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    salary_min = django_filters.NumberFilter(
        field_name='salary_min', lookup_expr='gte', label='Payment from'
    )
    location = django_filters.MultipleChoiceFilter(
        choices=lambda: get_choices('location'),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    country = django_filters.MultipleChoiceFilter(
        choices=lambda: get_choices('country'),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    # company = django_filters.ChoiceFilter(choices=lambda: JobPostingFilter.get_choices('company'))
    sort_by = django_filters.ChoiceFilter(
        choices=[('created', 'Oldest to Newest'), ('-created', 'Newest to Oldest')],
        method='filter_by_sort', label='Sort by'
    )

    class Meta:
        model = JobPosting
        fields = [
            'domain',
            'company_type',
            'experience_years',
            'english_level',
            'accept_region',
            'remote_type',
            'salary_min',
            'country',
            'location',
            # 'company',
            
        ]

    
    def filter_by_sort(self, queryset, name, value):
        return queryset.order_by(value)