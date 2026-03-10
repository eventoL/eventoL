from django import template

register = template.Library()

@register.simple_tag
def render_bundle(bundle_name, *args, **kwargs):
    return ''

