from django import template
from django.utils.safestring import mark_safe
from django.templatetags.static import static

register = template.Library()

@register.simple_tag
def tailwind_css():
    return mark_safe(
        f'<link rel="stylesheet" href="{static("css/tailwind.css")}">'
    ) 