from django.shortcuts import render

from jobs.models import JobPosting
from jobs.utils import filter_by_query, filter_by_any_keywords, filter_by_exclude_keywords, paginate_jobs

import random
from django.db import transaction


def jobs_list(request):
    JOBS_PER_PAGE = 20

    jobs = JobPosting.objects.all()

    q = request.GET.get("q", "")
    search_type = request.GET.get("search_type", "")
    position_only = request.GET.get("position_only", "") == "on"
    description_only = request.GET.get("description_only", "") == "on"
    any_keywords = request.GET.get("any_keywords", "")
    exclude_keywords = request.GET.get("exclude_keywords", "")

    jobs = filter_by_query(jobs, q, position_only, description_only)
    jobs = filter_by_any_keywords(jobs, any_keywords)
    jobs = filter_by_exclude_keywords(jobs, exclude_keywords)

    page = request.GET.get("page", 1)
    jobs_list, paginator = paginate_jobs(jobs, page, JOBS_PER_PAGE)

    return render(request, "jobs/list.html", {
        "jobs": jobs_list,
        "paginator": paginator,
        "page_obj": jobs_list,
        "is_paginated": jobs_list.has_other_pages(),
    })