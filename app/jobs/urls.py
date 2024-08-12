from django.urls import path
from .views import JobPostingListView, JobPostingDetailView

urlpatterns = [
    path('', JobPostingListView.as_view(), name='jobs_list'),
    path('job/<int:pk>/', JobPostingDetailView.as_view(), name='job_posting_detail'),
]
