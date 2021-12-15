from django import template
from django.utils.safestring import mark_safe
from json2html import json2html


register = template.Library()


@register.filter(name="json2html")
def convert_json_to_html(value,):
    return mark_safe(json2html.convert(value))
