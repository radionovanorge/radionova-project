from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def tailwind_css():
    return mark_safe(
        '<link rel="stylesheet" href="/static/css/tailwind.css">'
    ) 