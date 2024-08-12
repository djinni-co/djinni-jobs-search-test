from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from .models import JobPosting, Experience
from .forms import JobFilterForm
from django.db.models import Q


class JobPostingListView(ListView):
    model = JobPosting
    template_name = 'jobs/list.html'
    context_object_name = 'jobs'
    paginate_by = 20

    def get_queryset(self):
        form = JobFilterForm(self.request.GET)
        jobs = JobPosting.objects.all()

        if form.is_valid():
            cleaned_data = form.cleaned_data

            filters = Q()

            if cleaned_data.get('q'):
                filters &= Q(position__icontains=cleaned_data['q']) | Q(long_description__icontains=cleaned_data['q'])
            if cleaned_data.get('position'):
                filters &= Q(position__icontains=cleaned_data['position'])
            if cleaned_data.get('long_description'):
                filters &= Q(long_description__icontains=cleaned_data['long_description'])
            if cleaned_data.get('primary_keyword'):
                filters &= Q(primary_keyword__icontains=cleaned_data['primary_keyword'])
            if cleaned_data.get('secondary_keyword'):
                filters &= Q(secondary_keyword__icontains=cleaned_data['secondary_keyword'])
            if cleaned_data.get('extra_keywords'):
                filters &= Q(extra_keywords__icontains=cleaned_data['extra_keywords'])

            if cleaned_data.get('salary_min') is not None:
                filters &= Q(salary_min__gte=cleaned_data['salary_min'])
            if cleaned_data.get('salary_max') is not None:
                filters &= Q(salary_max__lte=cleaned_data['salary_max'])

            if cleaned_data.get('remote_type'):
                filters &= Q(remote_type=cleaned_data['remote_type'])

            if cleaned_data.get('country'):
                filters &= Q(country__icontains=cleaned_data['country'])
            if cleaned_data.get('location'):
                filters &= Q(location__icontains=cleaned_data['location'])

            if cleaned_data.get('english_level'):
                if cleaned_data['english_level'] == 'no_english':
                    filters &= Q(english_level='no_english') | Q(english_level__isnull=True) | Q(english_level='')
                else:
                    filters &= Q(english_level=cleaned_data['english_level'])

            if cleaned_data.get('experience_years'):
                if cleaned_data['experience_years'] == 'no_experience':
                    filters &= Q(experience_years='no_experience') | Q(experience_years__isnull=True) | Q(experience_years='')
                else:
                    filters &= Q(experience_years=cleaned_data['experience_years'])

            if cleaned_data.get('company_name'):
                filters &= Q(company__name__icontains=cleaned_data['company_name'])

            jobs = jobs.filter(filters)

        return jobs

    def get_context_data(self, **kwargs):
        context = super(JobPostingListView, self).get_context_data(**kwargs)
        context['form'] = JobFilterForm(self.request.GET or None)
        return context

class JobPostingDetailView(DetailView):
    model = JobPosting
    template_name = 'jobs/job_posting_detail.html'
    context_object_name = 'job'
