from django import template
from django.utils.translation import gettext_lazy as _
register = template.Library()


@register.filter
def trans(value):
    print(value, _(value))
    return _(value)
