from django import template

register = template.Library()


@register.filter
def get_request_list(dictionary, key):
    return dictionary.getlist(key)
