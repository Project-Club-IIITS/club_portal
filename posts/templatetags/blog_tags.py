from django import template
from posts.models import Post

register = template.Library()

@register.filter
def clubslug(value):
    print(value)
    return value.replace(' ','-')
