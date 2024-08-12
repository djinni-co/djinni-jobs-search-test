from django.urls import path

from jobs import views


urlpatterns = [
    path("", views.JobsListView.as_view(), name="jobs_list"),
]
