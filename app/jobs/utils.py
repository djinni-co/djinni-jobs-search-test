from django.db.models import Model

from jobs.models import JobPosting

def get_unique_choices(field_name: str, model: Model):
    """
    Fetches unique values from the specified field in the given model,
    cleans them, and formats them as a list of tuples for the ChoiceFilter.
    
    Parameters:
        field_name (str): The name of the field to fetch unique values from.
        model (Model): The Django model to query.

    Returns:
        list: A list of tuples with unique choices.
    """
    values = model.objects.values_list(field_name, flat=True).distinct()

    cleaned_values = set()
    for value in values:
        if value:
            try:

                cleaned_value = int(value)
            except (ValueError, TypeError):
                cleaned_value = value

            cleaned_values.add(cleaned_value)

    # Format choices as a list of tuples
    choices = sorted([(val, val) for val in cleaned_values])
    return choices


def get_choices(field_name):
    """
    Fetches unique values from the specified field and formats them as a list of tuples for the ChoiceFilter.

    Parameters:
        field_name (str): The name of the field to fetch choices from.

    Returns:
        list: A list of tuples for use in the ChoiceFilter.
    """
    
    values = JobPosting.objects.values_list(field_name, flat=True).distinct()

    choices = set()
    for value in values:
        if value:  
            if ',' in value:
                items = [item.strip() for item in value.split(',') if item.strip()]
                choices.update(items)
            else:
                choices.add(value.strip())

    
    return sorted([(item, item) for item in choices])