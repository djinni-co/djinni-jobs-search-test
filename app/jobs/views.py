from django.core.paginator import Paginator
from django.db.models import Max
from django.shortcuts import render

from .filters import JobPostingFilter
from .models import JobPosting


def jobs_list(request):
    JOBS_PER_PAGE = 20

    sort_by = request.GET.get("sort", "date_desc")
    if sort_by not in ["date_desc", "date_asc", "views_desc", "views_asc"]:
        sort_by = "date_desc"

    sorted_jobs = JobPosting.objects.all()

    # Apply sorting based on the sort_by parameter
    if sort_by == "views_asc":
        sorted_jobs = sorted_jobs.order_by("views_count")
    elif sort_by == "views_desc":
        sorted_jobs = sorted_jobs.order_by("-views_count")
    elif sort_by == "date_asc":
        sorted_jobs = sorted_jobs.order_by("published")
    else:
        sorted_jobs = sorted_jobs.order_by("-published")

    job_filter = JobPostingFilter(request.GET, queryset=sorted_jobs)

    paginator = Paginator(job_filter.qs, JOBS_PER_PAGE)
    page = request.GET.get("page")
    jobs_list = paginator.get_page(page)

    # Get the maximum salary to use in filter
    max_salary = (
        JobPosting.objects.aggregate(Max("salary_max"))["salary_max__max"] or 0
    )

    return render(
        request,
        "jobs/list.html",
        {
            "jobs": jobs_list,
            "filter": job_filter,
            "max_salary": max_salary,
            "sort_by": sort_by,
        },
    )
