from django.core.paginator import Paginator
from django.shortcuts import render

from jobs.models import JobPosting, Company

import random
from django.db import transaction

def jobs_list(request):
    JOBS_PER_PAGE = 20

    jobs = JobPosting.objects.all()
    page = int(request.GET.get("page", 1)) or 1
    paginator = Paginator(jobs, JOBS_PER_PAGE)
    jobs_list = paginator.page(page)

    return render(request, "jobs/list.html", { "jobs": jobs_list })
