import django_filters
import pycountry
from django.db.models import Q

from jobs.models import JobPosting, EnglishLevel


class JobsFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search")
    salary = django_filters.NumberFilter(method="filter_salary")
    english_level = django_filters.ChoiceFilter(choices=EnglishLevel.choices, method="filter_english_level")
    country = django_filters.CharFilter(method="filter_country")

    @staticmethod
    def filter_search(queryset, name, value):
        query_list = (
            "position__icontains",
            "long_description__icontains",
            "primary_keyword__icontains",
            "secondary_keyword__icontains",
            "extra_keywords__icontains",
            "company__name__icontains"
        )
        query_filter = Q()
        for query in query_list:
            query_filter |= Q(**{query:value})
        return queryset.filter(query_filter)

    @staticmethod
    def filter_salary(queryset, name, value):
        return queryset.filter(salary_min__lte=value, salary_max__gte=value)

    @staticmethod
    def filter_english_level(queryset, name, value):
        """
        Assume that chosen english level is 'pre'.
        In that case, other lower levels of English knowledge can be also shown.
        """
        levels_list = EnglishLevel.values
        max_level = levels_list.index(value)
        # filter job postings from "no english" to max level of knowledge
        return queryset.filter(english_level__in=levels_list[:max_level+1])

    @staticmethod
    def filter_country(queryset, name, value):
        country = pycountry.countries.search_fuzzy(value)[0]
        if not country:
            return queryset
        return queryset.filter(country__icontains=country.alpha_3)

    class Meta:
        model = JobPosting
        fields = ["remote_type"]
