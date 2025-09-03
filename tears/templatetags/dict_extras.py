from django import template


register = template.Library()

@register.filter
def dict_get(d, key):
    return d.get(key)

@register.filter
def make_range(value, arg):
    try:
        return range(int(value), int(arg))
    except:
        return []
@register.filter
def index(sequence, position):
    try:
        return sequence[position]
    except:
        return None

@register.simple_tag
def dict_set(d, args):
    """
    Sets a value in a nested dict.
    Usage in template: {{ some_dict|dict_set:"key,value" }}
    """
    try:
        key, value = args.split(',')
        d[key] = value
        return d
    except Exception:
        return d
    
@register.filter
def lookup(d, key):
    try:
        return d.get(key)
    except (AttributeError, TypeError):
        return None