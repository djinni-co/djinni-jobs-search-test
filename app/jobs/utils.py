from typing import Tuple

from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, Page
from django import forms
from functools import reduce
import operator
from django.db.models.query import QuerySet
import re


def word_boundary_regex(word: str) -> str:
    """
    Create regular expression to find word boundary.
    Using this type since we use PostgreSQL as db.
    """
    return r'\y{}\y'.format(re.escape(word))


def q_form_handler(jobs: QuerySet, form: forms.Form) -> QuerySet:
    """
    Handle job postings filtering and return filtered jobs
    """
    q = form.cleaned_data.get("q")
    search_position = form.cleaned_data.get("search_position")
    search_long_description = form.cleaned_data.get("search_long_description")
    any_keywords = form.cleaned_data.get("any_keywords")
    exclude_keywords = form.cleaned_data.get("exclude_keywords")

    jobs = filter_by_query(jobs, q, search_position, search_long_description)
    jobs = filter_by_any_keywords(jobs, any_keywords)
    jobs = filter_by_exclude_keywords(jobs, exclude_keywords)

    return jobs


def category_form_handler(jobs: QuerySet, form: forms.Form) -> Tuple[QuerySet, dict]:
    """
    Handle job postings filtering by category form user input and return tuple containing
    filtered job postings and predefined context(needed for template rendering)
    """
    category = form.cleaned_data.get("selected_category")
    remote_type = form.cleaned_data.get("selected_remote_type")
    english_level = form.cleaned_data.get("selected_english_level")
    #experience_level = form.cleaned_data.get("selected_experience_level")

    # Define the hierarchy of English levels
    english_level_hierarchy = {
        "fluent": ["fluent", "upper", "intermediate", "pre", "basic", "no_english"],
        "upper": ["upper", "intermediate", "pre", "basic", "no_english"],
        "intermediate": ["intermediate", "pre", "basic", "no_english"],
        "pre": ["pre", "basic", "no_english"],
        "basic": ["basic", "no_english"],
        "no_english": ["no_english"]
    }

    jobs = jobs.filter(primary_keyword__icontains=category)
    jobs = jobs.filter(remote_type__icontains=remote_type)
    if english_level in english_level_hierarchy:
        jobs = jobs.filter(english_level__in=english_level_hierarchy[english_level])
    #jobs = jobs.filter(primary_keyword__icontains=category)
    context = {
        "selected_category": category,
        "selected_remote_type": remote_type,
        "selected_english_level": english_level
    }

    return jobs, context


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
