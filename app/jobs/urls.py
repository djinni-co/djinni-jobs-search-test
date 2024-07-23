from django.urls import path

from jobs import views


urlpatterns = [
    path("", views.jobs_list, name="jobs_list"),
]
