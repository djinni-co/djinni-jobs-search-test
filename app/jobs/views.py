from django.core.paginator import Paginator
from django.shortcuts import render

from jobs.models import (JobPosting, Order, Country, Location, RemoteType, EnglishLevel, Experience, CompanyType,
                         CATEGORIES, SUBCATEGORIES)
from jobs.filters import JobFilterSchema

JOBS_PER_PAGE = 20


def jobs_list(request):

    job_filter = JobFilterSchema(request.GET, queryset=JobPosting.objects.filter(status=JobPosting.Status.PUBLISHED))

    jobs = job_filter.qs

    paginator = Paginator(jobs, JOBS_PER_PAGE)
    page_number = request.GET.get('page', 1)
    jobs = paginator.get_page(page_number)
    jobs.adjusted_elided_pages = paginator.get_elided_page_range(page_number)

    context = {
        # List of jobs
        'jobs': jobs,
        # Selected filters (query parameters)
        'search_text': job_filter.data.get('search_text', ''),
        'full_text_search': job_filter.data.get('full_text_search', ''),
        'company_name': job_filter.data.get('company_name', ''),
        'exclude_words': job_filter.data.get('exclude_words', ''),
        'order': job_filter.data.get('order', Order.PUBLISHED_NEW_TO_OLD),
        'salary_min': job_filter.data.get('salary_min', 0),
        'remote_type': job_filter.data.getlist('remote_type', []),
        'english_level': job_filter.data.getlist('english_level', []),
        'experience_years': job_filter.data.getlist('experience_years', []),
        'company_type': job_filter.data.getlist('company_type', []),
        'category': job_filter.data.get('category', ''),
        'subcategory': job_filter.data.get('subcategory', ''),
        'country': job_filter.data.getlist('country', []),
        'location':
            job_filter.data.getlist('location', []) if len(job_filter.data.getlist('country', [])) == 1 and
            job_filter.data.getlist('country')[0] == Country.UKRAINE
            else [],
        # Choices for filters
        'orders': Order.choices,
        'remote_type_choices': RemoteType.choices,
        'english_level_choices': EnglishLevel.choices,
        'experience_choices': Experience.choices,
        'company_type_choices': CompanyType.choices,
        'category_choices': CATEGORIES,
        'subcategory_choices': SUBCATEGORIES,
        'country_choices': Country.choices,
        'location_choices': Location.choices
    }

    return render(request, 'jobs/list.html', context)
