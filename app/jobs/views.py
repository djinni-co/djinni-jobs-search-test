from django.shortcuts import render

from jobs.models import JobPosting
from jobs.utils import filter_by_query, filter_by_any_keywords, filter_by_exclude_keywords, paginate_jobs
from jobs.forms import JobFilterForm
import random
from django.db import transaction


def jobs_list(request):
    JOBS_PER_PAGE = 20
    form = JobFilterForm(request.GET)

    jobs = JobPosting.objects.all()

    if form.is_valid():
        q = form.cleaned_data.get("q")
        search_position = form.cleaned_data.get("search_position")
        search_long_description = form.cleaned_data.get("search_long_description")
        any_keywords = form.cleaned_data.get("any_keywords")
        exclude_keywords = form.cleaned_data.get("exclude_keywords")

        jobs = filter_by_query(jobs, q, search_position, search_long_description)
        jobs = filter_by_any_keywords(jobs, any_keywords)
        jobs = filter_by_exclude_keywords(jobs, exclude_keywords)

    page = request.GET.get("page", 1)
    jobs_list, paginator = paginate_jobs(jobs, page, JOBS_PER_PAGE)

    # Construct the querystring for pagination links
    querystring = request.GET.copy()
    if 'page' in querystring:
        querystring.pop('page')
    querystring = querystring.urlencode()

    return render(request, "jobs/list.html", {
        "form": form,
        "jobs": jobs_list,
        "paginator": paginator,
        "page_obj": jobs_list,
        "is_paginated": jobs_list.has_other_pages(),
        "querystring": querystring,
    })
