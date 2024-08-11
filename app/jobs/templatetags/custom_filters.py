from django import template
import re

register = template.Library()


@register.filter
def highlight(text: str, search: str) -> str:
    """This func is used to highlight searched text"""
    if not search:
        return text
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    highlighted_text = pattern.sub(
        lambda match: f'<span class="highlight">{match.group(0)}</span>', text
    )
    return highlighted_text
