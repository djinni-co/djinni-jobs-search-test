from django.urls import path
from .views import jobs_list

urlpatterns = [
    path('jobs/', jobs_list, name='jobs_list'),
]
