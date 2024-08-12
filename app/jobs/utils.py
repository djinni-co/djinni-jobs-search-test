from django.db.models import Model

from jobs.models import JobPosting

def fetch_and_clean_values(field_name,model):
    """
    Fetches unique values from the specified field in the given model
    and cleans them by converting to int where applicable or splitting by comma.

    Parameters:
        field_name (str): The name of the field to fetch unique values from.
        model (Model): The Django model to query.

    Returns:
        set: A set of cleaned unique values.
    """
    values = model.objects.values_list(field_name, flat=True).distinct()

    cleaned_values = set()
    for value in values:
        if value:
            if isinstance(value, str) and ',' in value:
                items = [item.strip() for item in value.split(',') if item.strip()]
                cleaned_values.update(items)
            else:
                try:
                    cleaned_value = int(value)
                except (ValueError, TypeError):
                    cleaned_value = value
                cleaned_values.add(cleaned_value)

    return cleaned_values

def format_choices(cleaned_values):
    """
    Formats a set of cleaned values as a list of tuples for use in ChoiceFilter.

    Parameters:
        cleaned_values (set): A set of cleaned unique values.

    Returns:
        list: A sorted list of tuples formatted for ChoiceFilter.
    """
    return sorted([(val, val) for val in cleaned_values])

def get_unique_choices(field_name, model):
    """
    Fetches and formats unique choices from the specified field in the given model for ChoiceFilter.

    Parameters:
        field_name (str): The name of the field to fetch unique values from.
        model (Model): The Django model to query.

    Returns:
        list: A list of tuples with unique choices for ChoiceFilter.
    """
    cleaned_values = fetch_and_clean_values(field_name, model)
    return format_choices(cleaned_values)

def get_choices(field_name):
    """
    Fetches and formats unique choices from the specified field in the JobPosting model for ChoiceFilter.

    Parameters:
        field_name (str): The name of the field to fetch choices from.

    Returns:
        list: A list of tuples with choices for ChoiceFilter.
    """
    cleaned_values = fetch_and_clean_values(field_name, JobPosting)
    return format_choices(cleaned_values)
