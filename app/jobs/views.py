from django_filters.views import FilterView

from jobs.filters import JobsFilter
from jobs.models import JobPosting


class JobsListView(FilterView):
    queryset = JobPosting.objects.filter(status=JobPosting.Status.PUBLISHED.value)
    filterset_class = JobsFilter
    ordering = ("published",)
    paginate_by = 20
    template_name = "jobs/list.html"
