import django_filters

from django.db.models import Q

from jobs.models import (JobPosting, Order, Country, Location, RemoteType, EnglishLevel, CompanyType, Experience,
                         AcceptRegion, CATEGORIES, SUBCATEGORIES, EU_COUNTRY_CODES)


class JobFilterSchema(django_filters.FilterSet):
    search_text = django_filters.CharFilter(method='filter_search_text', label='Search', max_length=100)
    company_name = django_filters.CharFilter(method='filter_company_name', label='Company Name', max_length=50)
    exclude_words = django_filters.CharFilter(method='filter_exclude_words', label='Exclude Words', max_length=100)
    salary_min = django_filters.NumberFilter(method='filter_salary', label='Minimum Salary')
    remote_type = django_filters.MultipleChoiceFilter(choices=RemoteType.choices, method='filter_remote_type',
                                                      label='Remote Type')
    english_level = django_filters.MultipleChoiceFilter(choices=EnglishLevel.choices, method='filter_english_level',
                                                        label='English Level')
    experience_years = django_filters.MultipleChoiceFilter(choices=Experience.choices, method='filter_experience_years',
                                                           label='Experience Years')
    company_type = django_filters.MultipleChoiceFilter(choices=CompanyType.choices, method='filter_company_type',
                                                       label='Company Type')
    category = django_filters.ChoiceFilter(choices=[(value, key) for key, value in CATEGORIES.items()],
                                           method='filter_category', label='Category')
    country = django_filters.MultipleChoiceFilter(choices=Country.choices, method='filter_country',
                                                  label='Country')
    location = django_filters.MultipleChoiceFilter(choices=Location.choices, method='filter_location', label='Location')

    order = django_filters.OrderingFilter(choices=Order.choices, label='Order by')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically update subcategory values based on selected category
        self.subcategory_values = SUBCATEGORIES.get(self.data.get('category'), {}).values()

    @staticmethod
    def filter_company_name(queryset, _, value):
        if value:
            return queryset.filter(company__name__trigram_word_similar=value)
        return queryset

    @staticmethod
    def filter_salary(queryset, _, value):
        if value and value > 0:
            queryset = queryset.filter(
                Q(salary_max__gte=value) |
                Q(salary_min__lte=value, salary_max__gte=value) |
                Q(public_salary_max__gte=value) |
                Q(public_salary_min__lte=value, public_salary_max__gte=value)
            )
        return queryset

    @staticmethod
    def filter_remote_type(queryset, _, value):
        if value:
            return queryset.filter(remote_type__in=value)
        return queryset

    @staticmethod
    def filter_english_level(queryset, _, value):
        if value:
            return queryset.filter(english_level__in=value)
        return queryset

    @staticmethod
    def filter_experience_years(queryset, _, value):
        if value:
            years = [float(v.replace('y', '')) for v in value]

            if 0 in years:
                years.append(0.5)

            return queryset.filter(experience_years__in=years)
        return queryset

    @staticmethod
    def filter_company_type(queryset, _, value):
        if value:
            return queryset.filter(company_type__in=value)
        return queryset

    @staticmethod
    def filter_country(queryset, _, value):
        if value:
            if Country.UKRAINE not in value:
                queryset = queryset.exclude(accept_region=AcceptRegion.UKRAINE)

            if Country.EUROPE in value:
                value.remove(Country.EUROPE)
                value.extend(EU_COUNTRY_CODES)

            query = Q()
            for country in value:
                query |= Q(country__icontains=country)

            return queryset.filter(query | Q(country__isnull=True))
        return queryset

    def filter_search_text(self, queryset, _, value):
        if value:
            if self.data.get('full_text_search', '') == 'on':
                return queryset.filter(Q(position__trigram_word_similar=value) |
                                       Q(long_description__search=value) |
                                       Q(primary_keyword__trigram_word_similar=value) |
                                       Q(secondary_keyword__trigram_word_similar=value) |
                                       Q(extra_keywords__trigram_word_similar=value))

            return queryset.filter(position__trigram_word_similar=value)
        return queryset

    def filter_exclude_words(self, queryset, _, value):
        if value:
            exclude_words = [word.strip() for word in value.split()]
            exclude_query = Q()

            if self.data.get('full_text_search', '') == 'on':
                for word in exclude_words:
                    exclude_query |= Q(position__trigram_word_similar=word) | \
                                     Q(long_description__search=word) | \
                                     Q(primary_keyword__trigram_word_similar=word) | \
                                     Q(secondary_keyword__trigram_word_similar=word) | \
                                     Q(extra_keywords__trigram_word_similar=word)

                return queryset.exclude(exclude_query)

            for word in exclude_words:
                exclude_query |= Q(position__trigram_word_similar=word)

            return queryset.exclude(exclude_query)
        return

    def filter_category(self, queryset, _, value):
        if value:
            if self.data.get('subcategory') and self.data['subcategory'] in self.subcategory_values:
                return queryset.filter(primary_keyword=self.data['subcategory'])
            elif self.subcategory_values:
                return queryset.filter(primary_keyword__in=self.subcategory_values)
            return queryset.filter(primary_keyword=value)
        return queryset

    def filter_location(self, queryset, _, value):
        if value and len(self.data.getlist('country', [])) == 1 and Country.UKRAINE in self.data['country']:
            query = Q()
            for val in value:
                query |= Q(location__icontains=val)

            query |= Q(Q(country__icontains=Country.UKRAINE) & ~Q(location__isnull=True))
            query |= Q(Q(country__isnull=True) & ~Q(accept_region=AcceptRegion.EUROPE_ONLY))

            return queryset.filter(query)
        return queryset
