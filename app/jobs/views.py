from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from .filters import JobPostingFilterSet
from .models import JobPosting
from .paginations import JobPostingPagination
from .serializers import JobPostingSerializer


class JobPostingViewSet(viewsets.ModelViewSet):
    queryset = JobPosting.objects.select_related('company').all()
    serializer_class = JobPostingSerializer

    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    search_fields = [
        'position',
        'long_description',
        'primary_keyword',
        'secondary_keyword',
        'extra_keywords',
        'location',
        'company__name',
    ]
    ordering_fields = [
        'salary_min',
        'salary_max',
        'position',
        '-salary_min',
        '-salary_max',
        '-position',
        'published',
        'applications_count',
    ]
    filterset_class = JobPostingFilterSet
    pagination_class = JobPostingPagination

    def get_queryset(self):
        queryset = super().get_queryset().select_related('company')
        queryset = self.filter_queryset(queryset)

        # Custom logic using include_terms and exclude_terms for this:
        # Додайте можливість додавати блок слова: наприклад, я шукаю AQA Python, але не Java. Або треба виключити Fullstack вакансії зі списку.
        include_terms = self.request.GET.get('include_terms', '')
        exclude_terms = self.request.GET.get('exclude_terms', '')

        if include_terms:
            include_query = Q()
            for term in include_terms.split():
                include_query |= (
                        Q(position__icontains=term) |
                        Q(location__icontains=term) |
                        Q(long_description__icontains=term) |
                        Q(primary_keyword__icontains=term) |
                        Q(secondary_keyword__icontains=term) |
                        Q(extra_keywords__icontains=term) |
                        Q(company__name__icontains=term)
                )
            queryset = queryset.filter(include_query)

        if exclude_terms:
            exclude_query = Q()
            for term in exclude_terms.split():
                exclude_query |= (
                        Q(position__icontains=term) |
                        Q(location__icontains=term) |
                        Q(long_description__icontains=term) |
                        Q(primary_keyword__icontains=term) |
                        Q(secondary_keyword__icontains=term) |
                        Q(extra_keywords__icontains=term) |
                        Q(company__name__icontains=term)
                )
            queryset = queryset.exclude(exclude_query)

        return queryset.order_by('-published')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


def jobs_list(request):
    queryset = JobPosting.objects.select_related('company').all()

    search_query = request.GET.get('q', '')
    include_terms = request.GET.get('include_terms', '')
    exclude_terms = request.GET.get('exclude_terms', '')
    ordering = request.GET.get('ordering', '-published')

    if search_query:
        search_query = search_query.strip()
        queryset = queryset.filter(
            Q(position__icontains=search_query) |
            Q(long_description__icontains=search_query) |
            Q(primary_keyword__icontains=search_query) |
            Q(secondary_keyword__icontains=search_query) |
            Q(extra_keywords__icontains=search_query) |
            Q(company__name__icontains=search_query)
        )

    if include_terms:
        include_query = Q()
        for term in include_terms.split():
            include_query |= (
                Q(position__icontains=term) |
                Q(long_description__icontains=term) |
                Q(primary_keyword__icontains=term) |
                Q(secondary_keyword__icontains=term) |
                Q(extra_keywords__icontains=term) |
                Q(company__name__icontains=term)
            )
        queryset = queryset.filter(include_query)

    if exclude_terms:
        exclude_query = Q()
        for term in exclude_terms.split():
            exclude_query |= (
                Q(position__icontains=term) |
                Q(long_description__icontains=term) |
                Q(primary_keyword__icontains=term) |
                Q(secondary_keyword__icontains=term) |
                Q(extra_keywords__icontains=term) |
                Q(company__name__icontains=term)
            )
        queryset = queryset.exclude(exclude_query)

    filterset = JobPostingFilterSet(request.GET, queryset=queryset)
    queryset = filterset.qs

    ordering_fields = [
        'salary_min',
        'salary_max',
        'position',
        '-salary_min',
        '-salary_max',
        '-position',
        'published',
        '-published',
        'applications_count',
    ]

    if ordering in ordering_fields:
        queryset = queryset.order_by(ordering)
    else:
        queryset = queryset.order_by('-published')

    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'jobs': page_obj.object_list,
        'is_paginated': page_obj.has_other_pages(),
        'paginator': paginator,
        'page_obj': page_obj,
        'filterset': filterset,
    }

    return render(request, 'jobs/list.html', context)
