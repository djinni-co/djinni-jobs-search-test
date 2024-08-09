from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from .views import JobPostingViewSet

router = DefaultRouter()
router.register(r'jobpostings', JobPostingViewSet, basename='jobposting')

urlpatterns = [
    path('api/', include(router.urls)),  # Django REST framework API with filters etc.
    path('jobs_list/', views.jobs_list, name='jobs_list'),  # Rendering page with the same filters etc.
]
