import django_filters
from django.db.models import Q
from .models import JobPosting


class JobPostingFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method="filter_by_all_fields", label="Search"
        )
    keyword_search = django_filters.CharFilter(
        method="filter_by_keywords", label="Keywords"
    )
    exclude_keywords = django_filters.CharFilter(
        method="filter_by_exclude_keywords", label="Exclude Words"
    )
    salary_max = django_filters.NumberFilter(
        field_name="salary_max", lookup_expr="lte", label="Max Salary"
    )

    remote_type = JobPosting._meta.get_field("remote_type").choices
    country = django_filters.CharFilter(
        field_name="country", lookup_expr="icontains"
        )
    location = django_filters.CharFilter(
        field_name="location", lookup_expr="icontains"
        )
    english_level = JobPosting._meta.get_field("english_level").choices
    experience_years = django_filters.NumberFilter(
        field_name="experience_years", lookup_expr="gte"
    )
    company_name = django_filters.CharFilter(
        field_name="company__name", lookup_expr="icontains"
    )
    domain = JobPosting._meta.get_field("domain").choices
    company_type = JobPosting._meta.get_field("company_type").choices

    class Meta:
        model = JobPosting
        fields = [
            "keyword_search",
            "salary_max",
            "remote_type",
            "location",
            "english_level",
            "experience_years",
            "company_name",
            "domain",
            "company_type",
            "exclude_keywords",
        ]

    def filter_by_all_fields(self, queryset, name, value):
        return queryset.filter(
            Q(position__icontains=value) | Q(long_description__icontains=value)
        )

    def filter_by_keywords(self, queryset, name, value):
        return queryset.filter(
            Q(primary_keyword__icontains=value)
            | Q(secondary_keyword__icontains=value)
            | Q(extra_keywords__icontains=value)
        )

    def filter_by_exclude_keywords(self, queryset, name, value):
        exclude_words = value.split()
        for word in exclude_words:
            queryset = queryset.exclude(
                Q(primary_keyword__icontains=word)
                | Q(secondary_keyword__icontains=word)
                | Q(extra_keywords__icontains=word)
            )
        return queryset
