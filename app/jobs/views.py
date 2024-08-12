from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from django.urls import reverse
from functools import reduce

from jobs.models import (
    JobPosting,
    Company,
    EnglishLevel,
    Experience,
    RemoteType,
    AcceptRegion,
    CompanyType,
    Country
)


def jobs_list(request):
    JOBS_PER_PAGE = 20
    context = {}

    jobs = JobPosting.objects.select_related('company').all()
    basic_keywords = request.GET.get('basic_keywords')
    salary_from = request.GET.get('salary_from')
    salary_to = request.GET.get('salary_to')
    english_level = request.GET.getlist('english_level')
    experience = request.GET.getlist('experience')
    remote_type = request.GET.getlist('remote_type')
    region = request.GET.getlist('region')
    company_type = request.GET.getlist('company_type')
    country = request.GET.get('country')
    is_mob_reservation = request.GET.get('is_mob_reservation')
    is_part_time = request.GET.get('is_part_time')
    is_ukraine_only = request.GET.get('is_ukraine_only')

    if basic_keywords:
        jobs = filter_by_basic_keywords(jobs, basic_keywords)

    if english_level:
        jobs = filter_with_none_value(jobs, english_level, 'english_level', EnglishLevel.NONE.value)

    if remote_type:
        jobs = jobs.filter(remote_type__in=remote_type)

    if experience:
        jobs = filter_experience(jobs, experience)

    if region:
        jobs = filter_with_none_value(jobs, region, 'accept_region', AcceptRegion.WORLDWIDE.value)

    if salary_from:
        jobs = jobs.filter(salary_min__gte=salary_from)

    if salary_to:
        jobs = jobs.filter(salary_max__lte=salary_to)

    if company_type:
        jobs = jobs.filter(company_type__in=company_type)

    if country:
        jobs = filter_by_country(jobs, country)

    if is_mob_reservation:
        jobs = jobs.filter(is_reserving_from_mobilisation=True)

    if is_part_time:
        jobs = jobs.filter(is_parttime=True)

    if is_ukraine_only:
        jobs = jobs.filter(is_ukraine_only=True)

    page = int(request.GET.get("page", 1)) or 1
    paginator = Paginator(jobs, JOBS_PER_PAGE)
    jobs_list = paginator.page(page)
    context['total_num_pages'] = paginator.num_pages
    context['jobs'] = jobs_list
    context['english_level_choices'] = EnglishLevel.choices
    context['experience_choices'] = Experience.choices
    context['remote_type_choices'] = RemoteType.choices
    context['region_choices'] = AcceptRegion.choices
    context['company_type_choices'] = CompanyType.choices
    context['country_choices'] = Country.choices
    context['query_params'] = get_query_params(request)

    return render(request, "jobs/list.html", context)


def get_query_params(request):
    query_params = request.GET.copy()
    query_params.pop('page', None)

    return f"{reverse('jobs_list')}?{query_params.urlencode()}"


def filter_experience(queryset, experience):
    years = list(map(float, experience))
    half_years = [value + 0.5 for value in years]
    queryset = queryset.filter(experience_years__in=half_years + years)

    return queryset


def filter_with_none_value(queryset, list_query_params, filter_field, form_choice):
    """
    In db exists records with 'None' value.
    queryset: QuerySet - filtered queryset before that moment
    query_params: list - list from 'Request.GET' by key
    filter_field: str - the field by which you want to filter
    form_choice: str - choice value from form
    """
    query_params_copy = list_query_params.copy()
    in_filter = f'{filter_field}__in'
    isnull_filter = f'{filter_field}__isnull'

    if form_choice not in query_params_copy:
        queryset = queryset.filter(**{in_filter: query_params_copy})
    else:
        if len(query_params_copy) > 1:
            query_params_copy.remove(form_choice)
            queryset = queryset.filter(
                Q(**{in_filter: query_params_copy}) |
                Q(**{isnull_filter: True})
            )
        else:
            queryset = queryset.filter(**{isnull_filter: True})

    return queryset


def filter_by_basic_keywords(queryset, query_params):
    search_words = query_params.replace(' ', ',').split(',')
    search_words = list(filter(None, search_words)) # remove unnecessary ''
    filter_fields = (
        'position',
        'company__name',
        'extra_keywords',
        'secondary_keyword',
        'primary_keyword'
    )
    q_filters = Q()

    for field in filter_fields:
        q_filters |= reduce(
            lambda x, y: x | y,
            [Q(**{f'{field}__icontains': word}) for word in search_words]
        )

    queryset = queryset.filter(q_filters)

    return queryset


def filter_by_country(queryset, query_params):
    if query_params != Country.OTHER.value:
        queryset = queryset.filter(country__contains=query_params)
    else:
        q_filters = Q()
        exclude_countries = [ch[0] for ch in Country.choices if ch[0] != Country.OTHER.value]

        for country in exclude_countries:
            q_filters |= Q(**{'country__contains': country})

        queryset = queryset.exclude(q_filters)

    return queryset
