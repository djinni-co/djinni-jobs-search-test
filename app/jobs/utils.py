import re

from django.db.models import Q


def get_include_query(include_terms):
    include_query = Q()
    for term in include_terms:
        escaped_term = re.escape(term)
        include_query &= (
            Q(position__iregex=fr'{escaped_term}') |
            Q(long_description__iregex=fr'{escaped_term}') |
            Q(primary_keyword__iregex=fr'{escaped_term}') |
            Q(secondary_keyword__iregex=fr'{escaped_term}') |
            Q(extra_keywords__iregex=fr'{escaped_term}')
        )
    return include_query


def get_exclude_query(exclude_terms):
    exclude_query = Q()
    for term in exclude_terms:
        exclude_query &= (
            Q(position__icontains=term) |
            Q(long_description__icontains=term) |
            Q(primary_keyword__icontains=term) |
            Q(secondary_keyword__icontains=term) |
            Q(extra_keywords__icontains=term)
        )
    return exclude_query


def get_full_match_rank_query(include_terms):
    full_match_rank = Q()
    for term in include_terms:
        full_match_rank |= (
            Q(position__iexact=term) |
            Q(long_description__iexact=term) |
            Q(primary_keyword__iexact=term) |
            Q(secondary_keyword__iexact=term) |
            Q(extra_keywords__iexact=term)
        )
    return full_match_rank


def get_partial_match_rank_query(include_terms):
    partial_match_rank = Q()
    for term in include_terms:
        partial_match_rank |= (
            (Q(position__icontains=term) & ~Q(position__iexact=term)) |
            (Q(long_description__icontains=term) & ~Q(long_description__iexact=term)) |
            (Q(primary_keyword__icontains=term) & ~Q(primary_keyword__iexact=term)) |
            (Q(secondary_keyword__icontains=term) & ~Q(secondary_keyword__iexact=term)) |
            (Q(extra_keywords__icontains=term) & ~Q(extra_keywords__iexact=term))
        )
    return partial_match_rank


def separate_terms(terms):
    include_terms = [term for term in terms if not term.startswith('-')]
    exclude_terms = [term[1:] for term in terms if term.startswith('-')]
    return include_terms, exclude_terms


def apply_additional_filters(jobs, experience_years, english_level, salary_min, salary_max,
                             company_type, remote_type, job_domain, sort_by):

    if experience_years is not None:
        jobs = jobs.filter(experience_years=experience_years)

    if english_level:
        jobs = jobs.filter(english_level=english_level)

    if salary_min is not None:
        jobs = jobs.filter(salary_min__gte=salary_min)

    if salary_max is not None and salary_max >= salary_min:
        jobs = jobs.filter(salary_max__lte=salary_max)

    if company_type:
        jobs = jobs.filter(company_type=company_type)

    if remote_type:
        jobs = jobs.filter(remote_type__exact=remote_type)

    if job_domain:
        jobs = jobs.filter(domain__exact=job_domain)


    # Prioritize ranking, then sort by the user selected option

    if sort_by == 'date_asc':
        jobs = jobs.order_by('-full_match_rank', '-partial_match_rank', 'published')
    elif sort_by == 'date_desc':
        jobs = jobs.order_by('-full_match_rank', '-partial_match_rank', '-published')
    elif sort_by == 'reviews_asc':
        jobs = jobs.order_by('-full_match_rank', '-partial_match_rank', 'reviews_count')
    elif sort_by == 'reviews_desc':
        jobs = jobs.order_by('-full_match_rank', '-partial_match_rank', '-reviews_count')
    else:
        jobs = jobs.order_by('-full_match_rank', '-partial_match_rank')

    return jobs
