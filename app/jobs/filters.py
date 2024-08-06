from django_filters import FilterSet, NumberFilter, MultipleChoiceFilter, ChoiceFilter
from .models import JobPosting, get_primary_keywords_to_choices


class JobPostingFilter(FilterSet):
    EXPERIENCE_CHOICES = (
        (0, 'No Experience'),
        (0.5, 0.5),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10)
    )

    COUNTRY_CHOICES = (
        ('UKR', 'Ukraine'),
        ('DEU', 'Germany'),
        ('POL', 'Poland'),
        ('CZE', 'Czech'),
        ('HUN', 'Hungary')
    )

    LOCATION_CHOICES = (
        ('Киев', 'Kyiv'),
        ('Харьков', 'Kharkiv'),
        ('Ужгород', 'Uzhgorod'),
        ('Одеса', 'Odesa'),
        ('Львов', 'Lviv'),
        ('Днепр', 'Dnipro')
    )
    KEYWORD_CHOICES = get_primary_keywords_to_choices()

    experience_years = MultipleChoiceFilter(
        choices=EXPERIENCE_CHOICES
    )
    country = MultipleChoiceFilter(
        choices=COUNTRY_CHOICES
    )
    location = MultipleChoiceFilter(
        choices=LOCATION_CHOICES
    )
    primary_keyword = ChoiceFilter(
        choices=KEYWORD_CHOICES
    )
    public_salary_min = NumberFilter(
        label='Salary from',
        lookup_expr='gte'
    )

    class Meta:
        model = JobPosting
        fields = '__all__'
        exclude = [
            'position',
            'salary_min',
            'salary_max',
            'public_salary_max',
            'primary_keyword',
            'secondary_keyword',
            'extra_keywords',
            'long_description',
            'requires_cover_letter',
            'is_ukraine_only',
            'is_reserving_from_mobilisation',
            'unread_count',
            'search_count',
            'views_count',
            'applications_count',
            'sent_count',
            'recruiter',
            'status',
            'last_modified',
            'published',
            'created',
            'accept_region',
        ]

