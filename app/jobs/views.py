from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity

from jobs.models import JobPosting, Company

import random
from django.db import transaction
from django.core.cache import cache


def jobs_list(request):
    JOBS_PER_PAGE = 20

    page = int(request.GET.get("page", 1)) or 1
    query = request.GET.get('q', '')
    salary_min = request.GET.get('salary_min')
    salary_max = request.GET.get('salary_max')
    remote_types = request.GET.getlist('remote_type')
    country = request.GET.get('country')
    location = request.GET.get('location')
    english_level = request.GET.get('english_level')
    experience_years = request.GET.get('experience_years')

    jobs = JobPosting.objects.all()

    # Apply search filter
    if query:
        jobs = search(query)

    # Apply additional filters
    if salary_min:
        jobs = jobs.filter(public_salary_min__gte=salary_min)
    if salary_max:
        jobs = jobs.filter(public_salary_max__lte=salary_max)
    if remote_types:
        if any(rt in remote_types for rt in ['office', 'full_remote']):
            # add candidate_choice jobs based on logic that candidate choice already means having both office and
            # full_remote options
            remote_types.append('candidate_choice')
        jobs = jobs.filter(remote_type__in=remote_types)
    if country:
        jobs = search_by_country(country, jobs)
    if location:
        jobs = jobs.filter(location__icontains=location)
    if english_level:
        jobs = jobs.filter(english_level__iexact=english_level)
    if experience_years:
        jobs = search_by_experience(experience_years, jobs)

    paginator = Paginator(jobs, JOBS_PER_PAGE)
    jobs_list = paginator.get_page(page)
    total_pages = paginator.num_pages
    total_pages_list = list(range(1, total_pages + 1))
    context = {
        "jobs": jobs_list,
        "total_pages": total_pages,
        "current_page": page,
        "total_pages_list": total_pages_list,
        "remote_types": remote_types
    }

    return render(request, "jobs/list.html", context)


def search(query: str):
    cache_key = f'search_{query}'
    job_postings = cache.get(cache_key)
    if not job_postings:
        search_vector = (
                SearchVector('position', weight='A') +
                SearchVector('long_description', weight='D') +
                SearchVector('primary_keyword', weight='B') +
                SearchVector('secondary_keyword', weight='B') +
                SearchVector('extra_keywords', weight='C') +
                SearchVector('company__name', weight='A')
        )

        search_query = SearchQuery(query, search_type='websearch')

        job_postings = JobPosting.objects.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query),
            description_similarity=TrigramSimilarity('long_description', query),
            position_similarity=TrigramSimilarity('position', query)
        ).filter(
            search=search_query
        ).exclude(
            # parameters were empirically selected to achieve the most relevant search results
            Q(rank__lte=0.25, position_similarity__lt=0.4)
            # results with less rank do not represent the searched keywords
            | Q(rank__lte=0.1)
            # this line can be optional based on users' needs
            | Q(position_similarity__lte=0.2)
        ).order_by('-rank', '-position_similarity')

        cache.set(cache_key, job_postings, timeout=60 * 15)

    return job_postings


def search_by_country(country_query: str, job_postings):
    if country_query == 'ukraine':
        job_postings = job_postings.filter(
            Q(country__icontains='ukraine')
            | Q(is_ukraine_only=True)
            # not sure if custom_selection includes Ukraine region
            | Q(accept_region__in=['ukraine', 'europe', 'custom_selection'])
            | Q(company__country_code='UA')
        )
    else:
        job_postings = job_postings.filter(
            Q(country__icontains=country_query)
            | Q(company__country_code__icontains=country_query)
            # Additional filters for accept_region
            | Q(accept_region='worldwide')
            | Q(accept_region='custom_selection')
            # rare case when user prompts 'Europe' in country filter
            | Q(accept_region__icontains=country_query)
        )

    return job_postings


def search_by_experience(exp_option: str, job_postings):
    experience_ranges = {
        'no_exp': (0, 0),  # No experience
        '1y': (0, 1),  # Up to 1 year
        '2y': (1, 2),  # More than 1 year and up to 2 years
        '3y': (2, 3),  # More than 2 years and up to 3 years
        '5y': (3, float('inf'))  # More than 3 years
    }

    min_years, max_years = experience_ranges.get(exp_option, (0, float('inf')))
    job_postings = job_postings.filter(experience_years__gte=min_years, experience_years__lte=max_years)

    return job_postings
