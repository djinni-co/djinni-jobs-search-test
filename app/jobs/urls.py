from django.urls import path

from jobs import views


urlpatterns = [
    path("", views.jobs_list, name="jobs_list"),
    path("<int:pk>/", views.JobPostingDetailView.as_view(), name="job_detail"),
]

app_name = "jobs"
