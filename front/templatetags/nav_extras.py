from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def active(context, url_name):
    """
    Returns 'active' if the current page matches the given url_name.
    Usage: {% active 'home' %}
    """
    request = context['request']
    if request.resolver_match and request.resolver_match.url_name == url_name:
        return 'active'
    return ''
