import re

from django import template

register = template.Library()

@register.filter(name="replace_nbsp")
def replace_nbsp(value):
    """
    Replaces all occurrences of '&nbsp;' in the given string with a space character.

    Parameters:
        value (str): The input string to be processed.

    Returns:
        str: The processed string with '&nbsp;' replaced by a space character.
    """
    return re.sub(r'&nbsp;', ' ', value)

@register.filter(name='highlight')
def highlight(text, search_term):
    if not text or not search_term:
        return text

    escaped_search_term = re.escape(search_term)
    pattern = re.compile(r'({})'.format(escaped_search_term), re.IGNORECASE)
    
    highlighted_text = pattern.sub(r'<span class="highlight">\1</span>', text)
    
    return highlighted_text