from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Case, When, Value, IntegerField

from jobs.models import JobPosting, RemoteType, CompanyType, EnglishLevel, JobDomain

from jobs.utils import apply_additional_filters, separate_terms, get_include_query, get_exclude_query, \
    get_full_match_rank_query, get_partial_match_rank_query


def jobs_list(request):
    JOBS_PER_PAGE = 20

    context = {
        'english_level': EnglishLevel.choices,
        'job_domains': JobDomain.choices,
        'remote_type': RemoteType.choices,
        'company_type': CompanyType.choices,
    }

    jobs = JobPosting.objects.all()
    query = request.GET.get('q')

    experience_years = request.GET.get('experience_years')
    english_level = request.GET.get('english_level')
    salary_min = request.GET.get('salary_min')
    salary_max = request.GET.get('salary_max')
    remote_type = request.GET.get('remote_type')
    company_type = request.GET.get('company_type')
    job_domain = request.GET.get('job_domain')

    sort_by = request.GET.get('sort_by', 'date_desc')  # The most recent jobs are displayed by default

    if query:
        terms = query.split()
        include_terms, exclude_terms = separate_terms(terms)

        include_query = get_include_query(include_terms)
        exclude_query = get_exclude_query(exclude_terms)
        full_match_rank = get_full_match_rank_query(include_terms)
        partial_match_rank = get_partial_match_rank_query(include_terms)

        jobs = jobs.annotate(
            full_match_rank=Case(
                When(full_match_rank, then=Value(2)),
                default=Value(0),
                output_field=IntegerField(),
            ),
            partial_match_rank=Case(
                When(partial_match_rank, then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        ).filter(include_query).exclude(exclude_query)

        jobs = apply_additional_filters(jobs, experience_years, english_level, salary_min, salary_max,
                                        company_type, remote_type, job_domain, sort_by)

    page = int(request.GET.get("page", 1)) or 1
    paginator = Paginator(jobs, JOBS_PER_PAGE)
    jobs_list = paginator.page(page)

    return render(request, 'jobs/list.html', {'jobs': jobs_list, **context})
