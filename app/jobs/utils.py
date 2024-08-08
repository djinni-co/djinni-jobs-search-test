from typing import Tuple

from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, Page
from functools import reduce
import operator
from django.db.models.query import QuerySet


def filter_by_query(jobs: QuerySet, query: str, position_only: bool, description_only: bool) -> QuerySet:
    if query:
        query_list = query.split()
        query_list_q = reduce(operator.and_, [(
            Q(position__icontains=q) |
            Q(long_description__icontains=q) |
            Q(primary_keyword__icontains=q) |
            Q(secondary_keyword__icontains=q) |
            Q(extra_keywords__icontains=q)
        ) for q in query_list])
        jobs = jobs.filter(query_list_q)
        query_filter = Q()
        if position_only:
            query_filter |= reduce(operator.and_, [Q(position__icontains=q) for q in query_list])
        if description_only:
            query_filter |= reduce(operator.and_, [Q(long_description__icontains=q) for q in query_list])
        if position_only or description_only:
            jobs = jobs.filter(query_filter)
    return jobs


def filter_by_any_keywords(jobs: QuerySet, any_keywords: str) -> QuerySet:
    if any_keywords:
        any_keywords_list = any_keywords.split()
        any_keywords_q = reduce(operator.or_, [Q(position__icontains=keyword) for keyword in any_keywords_list])
        jobs = jobs.filter(any_keywords_q)
    return jobs


def filter_by_exclude_keywords(jobs: QuerySet, exclude_keywords: str) -> QuerySet:
    if exclude_keywords:
        exclude_keywords_list = exclude_keywords.split()
        exclude_keywords_q = reduce(operator.or_, [
            Q(position__icontains=keyword) |
            Q(long_description__icontains=keyword) |
            Q(primary_keyword__icontains=keyword) |
            Q(secondary_keyword__icontains=keyword) |
            Q(extra_keywords__icontains=keyword)
            for keyword in exclude_keywords_list
        ])
        jobs = jobs.exclude(exclude_keywords_q)
    return jobs


def paginate_jobs(jobs: QuerySet, page: int, jobs_per_page: int) -> Tuple[Page, Paginator]:
    paginator = Paginator(jobs, jobs_per_page)
    try:
        jobs_list = paginator.page(page)
    except PageNotAnInteger:
        jobs_list = paginator.page(1)
    except EmptyPage:
        jobs_list = paginator.page(paginator.num_pages)
    return jobs_list, paginator
