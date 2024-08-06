from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from jobs.models import JobPosting, Company

import random
from django.db import transaction

def jobs_list(request):
    JOBS_PER_PAGE = 20

    jobs = JobPosting.objects.all()
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
