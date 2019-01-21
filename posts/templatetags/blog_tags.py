from django import template
import re
import random

register = template.Library()


@register.filter
def clubslug(value):
    return value.replace(' ', '-')


@register.filter
def removeImg(value):
    print(value)
    p = re.compile(r'<img.*?/>')
    p = p.sub('', value)
    return p


@register.filter
def randomNumber(limit):
    return random.randint(1, limit)
