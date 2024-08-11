import logging
from annoying.decorators import render_to

from django.http import JsonResponse

from jobs.controllers.job_search import JobSearch


logger = logging.getLogger(__name__)
JOBS_PER_PAGE = 20


def search_jobs(request):
    job_search = JobSearch(request)
    return job_search.get_results()


@render_to("jobs/list.html")
def all_job_list(request):
    if request.is_ajax():
        jobs_list, jobs_count, has_next = search_jobs(request)
        jobs_data = [
            {
                'id': job.id,
                'position': job.position,
                'public_salary_max': job.public_salary_max,
                'company': job.company_name,
                'views_count': job.views_count,
                'applications_count': job.applications_count,
                'long_description': job.long_description
            }
            for job in jobs_list
        ]
        return JsonResponse(
            {
                "jobs": jobs_data,
                "jobs_count": jobs_count,
                "has_next": has_next
            }
        )
    else:
        jobs_list, jobs_count, has_next = search_jobs(request)
        context = {
            "jobs": jobs_list,
            "jobs_count": jobs_count,
            "has_next": has_next
            }
        return context
