from django.shortcuts import render

from jobs.models import JobPosting
from jobs.utils import q_form_handler, category_form_handler, order_form_handler, paginate_jobs, get_runtime_companies
from jobs.forms import JobFilterForm, CategoryFilterForm, OrderSelectionForm
import random
from django.db import transaction


def jobs_list(request):
    JOBS_PER_PAGE = 20
    form = JobFilterForm(request.GET)

    companies = get_runtime_companies()
    category_form = CategoryFilterForm(request.GET, companies)

    order_selection_form = OrderSelectionForm(request.GET)
    jobs = JobPosting.objects.all()

    context={}

    if form.is_valid():
        jobs = q_form_handler(jobs, form)

    if category_form.is_valid():
        jobs, context = category_form_handler(jobs, category_form, context.copy())

    if order_selection_form.is_valid():
        jobs, context = order_form_handler(jobs, order_selection_form, context.copy())

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
        "order_selection_form": order_selection_form,
        "jobs": jobs_list,
        "paginator": paginator,
        "page_obj": jobs_list,
        "is_paginated": jobs_list.has_other_pages(),
        "querystring": querystring,
        "companies": companies
    } | context

    return render(request, "jobs/list.html", render_context)
