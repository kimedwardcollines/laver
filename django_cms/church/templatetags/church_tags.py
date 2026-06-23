"""
Custom template tags for church templates
"""
from django import template

register = template.Library()


@register.filter
def get_logo_url(church):
    """Safely get church logo URL or return default"""
    if church and church.logo:
        return church.logo.url
    return '/static/images/church-bg.jpg'
