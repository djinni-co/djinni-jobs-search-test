from django.shortcuts import render

from jobs.models import JobPosting
from jobs.utils import q_form_handler, category_form_handler, paginate_jobs
from jobs.forms import JobFilterForm, CategoryFilterForm
import random
from django.db import transaction


def jobs_list(request):
    JOBS_PER_PAGE = 20
    form = JobFilterForm(request.GET)
    category_form = CategoryFilterForm(request.GET)
    jobs = JobPosting.objects.all()
    context={}

    if form.is_valid():
        jobs = q_form_handler(jobs, form)

    if category_form.is_valid():
        jobs, context = category_form_handler(jobs, category_form)

    page = request.GET.get("page", 1)
    jobs_list, paginator = paginate_jobs(jobs, page, JOBS_PER_PAGE)

    # Construct the querystring for pagination links
    querystring = request.GET.copy()
    if 'page' in querystring:
        querystring.pop('page')
    querystring = querystring.urlencode()

    render_context = {
        "form": form,
        "category_filter_form": category_form,
        "jobs": jobs_list,
        "paginator": paginator,
        "page_obj": jobs_list,
        "is_paginated": jobs_list.has_other_pages(),
        "querystring": querystring,
    } | context

    return render(request, "jobs/list.html", render_context)
