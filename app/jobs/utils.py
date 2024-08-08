from typing import Tuple

from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, Page
from functools import reduce
import operator
from django.db.models.query import QuerySet
import re


def word_boundary_regex(word: str) -> str:
    """
    Create regular expression to find word boundary.
    Using "\y" since we use PostgreSQL as db.
    """
    return r'\y{}\y'.format(re.escape(word))


def filter_by_query(jobs: QuerySet, query: str, position_only: bool, description_only: bool) -> QuerySet:
    """
    Initial filtering. Filter job postings by any match.
    If 'Search by Position' or 'Search by Long Description' checkboxes are on
    filter job postings accordingly.
    Switched to regular expressions to find exact matches
    """
    if query:
        query_list = re.split(r'[\W\s]+', query)
        query_list_q = reduce(operator.and_, [(
            Q(position__iregex=word_boundary_regex(q)) |
            Q(long_description__iregex=word_boundary_regex(q)) |
            Q(primary_keyword__iregex=word_boundary_regex(q)) |
            Q(secondary_keyword__iregex=word_boundary_regex(q)) |
            Q(extra_keywords__iregex=word_boundary_regex(q))
        ) for q in query_list])
        jobs = jobs.filter(query_list_q)
        query_filter = Q()
        if position_only:
            query_filter |= reduce(operator.and_, [
                Q(position__iregex=word_boundary_regex(q))
                for q in query_list])
        if description_only:
            query_filter |= reduce(operator.and_, [
                Q(long_description__iregex=word_boundary_regex(q))
                for q in query_list])
        if position_only or description_only:
            jobs = jobs.filter(query_filter)
    return jobs


def filter_by_any_keywords(jobs: QuerySet, any_keywords: str) -> QuerySet:
    """
    Additional filtering. Find word matches in positions.
    Switched to regular expressions to find exact matches
    """
    if any_keywords:
        any_keywords_list = re.split(r'[\W\s]+', any_keywords)
        any_keywords_q = reduce(operator.or_, [
            Q(position__iregex=word_boundary_regex(keyword))
            for keyword in any_keywords_list])
        jobs = jobs.filter(any_keywords_q)
    return jobs


def filter_by_exclude_keywords(jobs: QuerySet, exclude_keywords: str) -> QuerySet:
    """
    Additional filtering. Exclude job postings containing exclude_keywords.
    Switched to regular expressions to find exact matches
    """
    if exclude_keywords:
        exclude_keywords_list = re.split(r'[\W\s]+', exclude_keywords)
        exclude_keywords_q = reduce(operator.or_, [
            Q(position__iregex=word_boundary_regex(keyword)) |
            Q(long_description__iregex=word_boundary_regex(keyword)) |
            Q(primary_keyword__iregex=word_boundary_regex(keyword)) |
            Q(secondary_keyword__iregex=word_boundary_regex(keyword)) |
            Q(extra_keywords__iregex=word_boundary_regex(keyword))
            for keyword in exclude_keywords_list
        ])
        jobs = jobs.exclude(exclude_keywords_q)
    return jobs


def paginate_jobs(jobs: QuerySet, page: int, jobs_per_page: int) -> Tuple[Page, Paginator]:
    """
    Paginate filtered job postings.
    """
    paginator = Paginator(jobs, jobs_per_page)
    try:
        jobs_list = paginator.page(page)
    except PageNotAnInteger:
        jobs_list = paginator.page(1)
    except EmptyPage:
        jobs_list = paginator.page(paginator.num_pages)
    return jobs_list, paginator
