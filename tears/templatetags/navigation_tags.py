from django import template
from wagtail.models import Page

register = template.Library()

@register.simple_tag
def get_navbar_pages():
    return Page.objects.live().public().in_menu().filter(depth__gt=3)
    #return ['Item 1', 'Item 2', 'item 3']
    
@register.simple_tag
def get_root_page():
    return Page.objects.live().public().in_menu().first()