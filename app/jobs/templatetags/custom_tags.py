from datetime import timedelta, datetime, timezone
from django import template
from django.utils.dateformat import format

from jobs.models import LOCATION_CHOICES
from jobs.utils import alpha_3_to_country_name

register = template.Library()


@register.filter
def format_date(value):
    if not value:
        return ''

    today = datetime.now(timezone.utc).date()

    if value.date() == today:
        return 'Today'
    elif value.date() == (today - timedelta(days=1)):
        return 'Yesterday'
    else:
        return format(value, 'j M')


@register.filter
def format_experience_years(experience_years):
    if experience_years != 0:
        return f'{int(experience_years) if experience_years.is_integer() else experience_years} ' \
               f'year{"s" if experience_years > 1 else ""} of experience'
    return ''


@register.filter
def get_choice_label(value, choices):
    if value:
        return dict(choices)[value]
    return ''


@register.filter
def get_country_names(country: str | None) -> str:
    if country:
        return ', '.join([alpha_3_to_country_name(alpha_3_code) for alpha_3_code in country.split(',')])
    return ''


@register.filter
def get_location_names(location_names: str | None) -> str:
    if location_names:
        return f'({", ".join([LOCATION_CHOICES.get(location, location) for location in location_names.split(",")])})'
    return ''
