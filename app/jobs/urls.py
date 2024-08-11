from django.urls import path

from jobs import views

app_name = 'jobs'


urlpatterns = [
    path("", views.all_job_list, name="all_job_list"),
]
