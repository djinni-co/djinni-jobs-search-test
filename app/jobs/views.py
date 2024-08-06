from django.core.paginator import Paginator
from django.shortcuts import render

from jobs.models import JobPosting, Company
from .filters import JobPostingFilter
import random
from django.db import transaction


def jobs_list(request):
    JOBS_PER_PAGE = 20

    jobs = JobPosting.objects.all()
    if lookup_param := request.GET.get('q', ''):
        jobs = jobs.filter(position__icontains=lookup_param) | jobs.filter(long_description__icontains=lookup_param)
    if lookup_param := request.GET.get('primary_keyword', ''):
        jobs = jobs.filter(secondary_keyword__icontains=lookup_param) | jobs.filter(extra_keywords__icontains=lookup_param)
    f = JobPostingFilter(request.GET, queryset=jobs)
    page = int(request.GET.get("page", 1)) or 1
    paginator = Paginator(f.qs, JOBS_PER_PAGE)
    jobs = paginator.page(page)

    return render(request, "jobs/list.html", {"filter": f, "jobs": jobs}, )
