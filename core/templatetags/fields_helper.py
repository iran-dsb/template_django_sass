from django import template
from django.forms import RadioSelect, CheckboxInput

register = template.Library()

@register.filter('fieldtype')
def fieldtype(field):
    return field.field.widget.__class__.__name__

@register.filter(name='is_radio')
def is_radio(field):
    return field.field.widget.__class__.__name__ == RadioSelect().__class__.__name__

@register.filter(name='is_checkbox')
def is_checkbox(field):
    return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__
