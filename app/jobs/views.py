from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from jobs.models import JobPosting, Company

import random
from django.db import transaction

from django.db.models import Q


def jobs_list(request):
    JOBS_PER_PAGE = 20

    jobs = JobPosting.objects.all()

    q = request.GET.get("q", "")
    search_type = request.GET.get("search_type", "")
    any_keywords = request.GET.get("any_keywords", "")
    exclude_keywords = request.GET.get("exclude_keywords", "")

    if q:
        if search_type == "position":
            jobs = jobs.filter(position__icontains=q)
        elif search_type == "long_description":
            jobs = jobs.filter(long_description__icontains=q)
        else:
            jobs = jobs.filter(
                Q(position__icontains=q) |
                Q(long_description__icontains=q)
            )

    if any_keywords:
        any_keywords_list = any_keywords.split()
        any_keywords_q = Q()
        for keyword in any_keywords_list:
            any_keywords_q |= Q(position__icontains=keyword)
        jobs = jobs.filter(any_keywords_q)

    if exclude_keywords:
        exclude_keywords_list = exclude_keywords.split()
        exclude_keywords_q = Q()
        for keyword in exclude_keywords_list:
            exclude_keywords_q &= \
                Q(position__icontains=keyword) | \
                Q(long_description__icontains=keyword) | \
                Q(primary_keyword__icontains=keyword) | \
                Q(secondary_keyword__icontains=keyword) | \
                Q(extra_keywords__icontains=keyword)
        jobs = jobs.exclude(exclude_keywords_q)

    page = int(request.GET.get("page", 1)) or 1
    paginator = Paginator(jobs, JOBS_PER_PAGE)

    try:
        jobs_list = paginator.page(page)
    except PageNotAnInteger:
        jobs_list = paginator.page(1)
    except EmptyPage:
        jobs_list = paginator.page(paginator.num_pages)

    return render(request, "jobs/list.html", {
        "jobs": jobs_list,
        "paginator": paginator,
        "page_obj": jobs_list,
        "is_paginated": jobs_list.has_other_pages(),
    })