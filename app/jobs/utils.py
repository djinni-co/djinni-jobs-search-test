from typing import Tuple

from django.db.models import Q
from django.contrib.postgres.aggregates import StringAgg
from django.db.models import F
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


def category_form_handler(jobs: QuerySet, form: forms.Form, context_arg: dict) -> Tuple[QuerySet, dict]:
    """
    Handle job postings filtering by category form user input and return tuple containing
    filtered job postings and predefined context(needed for template rendering)
    """
    category = form.cleaned_data.get("selected_category")
    remote_type = form.cleaned_data.get("selected_remote_type")
    english_level = form.cleaned_data.get("selected_english_level")
    experience_level = form.cleaned_data.get("selected_experience_level")
    salary = form.cleaned_data.get("salary")

    if category != "":
        jobs = jobs.filter(primary_keyword=category)
    jobs = jobs.filter(remote_type__icontains=remote_type)
    jobs = english_selection_handler(jobs, english_level)
    jobs = experience_selection_handler(jobs, experience_level)
    if salary is not None:
        jobs = jobs.filter(salary_min__gte=salary)

    context = {
        "selected_category": category,
        "selected_remote_type": remote_type,
        "selected_english_level": english_level,
        "selected_experience_level": experience_level
    } | context_arg

    return jobs, context


def order_form_handler(jobs: QuerySet, form: forms.Form, context_arg: dict) -> Tuple[QuerySet, dict]:
    """
    Order job postings by applications or publishing dates
    """
    order = form.cleaned_data.get("selected_order")
    if order:
        jobs = jobs.order_by(f"-{order}")

    context = {
        "selected_order": order
    }

    return jobs, context | context_arg


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

def english_selection_handler(jobs: QuerySet, english_level: str) -> QuerySet:
    # Define the hierarchy of English levels
    english_level_hierarchy = {
        "fluent": ["fluent", "upper", "intermediate", "pre", "basic", "no_english"],
        "upper": ["upper", "intermediate", "pre", "basic", "no_english"],
        "intermediate": ["intermediate", "pre", "basic", "no_english"],
        "pre": ["pre", "basic", "no_english"],
        "basic": ["basic", "no_english"],
        "no_english": ["no_english"]
    }
    if english_level in english_level_hierarchy:
        jobs = jobs.filter(english_level__in=english_level_hierarchy[english_level])
    return jobs


def experience_selection_handler(jobs: QuerySet, experience_level: str) -> QuerySet:
    # Define exp levels as integers to integrate with user selection
    experience_level_hierarchy = {
        "no_exp": 0,
        "1y": 1,
        "2y": 2,
        "3y": 3,
        "5y": 5
    }

    # If User inputs 5y; find job postings with 5 years or greater level of exp
    # Else find job postings that correspond user selection with 1 year of error
    if experience_level in experience_level_hierarchy:
        if experience_level == "5y":
            jobs = jobs.filter(experience_years__gte=experience_level_hierarchy[experience_level])
        else:
            jobs = jobs.filter(
                Q(experience_years__gte=(experience_level_hierarchy[experience_level] - 1)) &
                Q(experience_years__lte=experience_level_hierarchy[experience_level])
            )

    return jobs