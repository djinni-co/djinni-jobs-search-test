import logging
from django.shortcuts import render
from django.core.paginator import Paginator

from jobs.models import JobPosting
from jobs.filters import JobPostingFilter
from jobs.services.search_service import JobSearchService

logger = logging.getLogger(__name__)

def jobs_list(request):
    """
    Handles the listing of job postings with search and filter functionality.
    
    Parameters:
        request (HttpRequest): The HTTP request object.
        
    Returns:
        HttpResponse: Rendered HTML template with job listings and filters.
    """
    JOBS_PER_PAGE = 20
    
    query = request.GET.get('q', '')
    
    if query:
        job_search_service = JobSearchService(query)
        search_results = job_search_service.search_jobs()
    else:
        search_results = JobPosting.objects.all()

    job_filter = JobPostingFilter(request.GET, queryset=search_results)
    filtered_jobs = job_filter.qs
    
    page_number = request.GET.get("page", 1)
    paginator = Paginator(filtered_jobs, JOBS_PER_PAGE)
    jobs_list = paginator.get_page(page_number)
    total_jobs = paginator.count

    return render(request, "jobs/list.html", {
        "jobs": jobs_list,
        "filter": job_filter,
        "query": query,
        "total_jobs": total_jobs,
    })