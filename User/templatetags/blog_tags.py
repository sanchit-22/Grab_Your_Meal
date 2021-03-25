from django import template

register=template.Library()

@register.filter(name='zip')
def zip_lists(a, b):
    return zip(a, b)

@register.filter(name='zipextract')
def zipextract(a):
    return a.objects.all()

@register.simple_tag
def zip_all(a, b, c):
    return zip(a, b, c)