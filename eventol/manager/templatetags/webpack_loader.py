from django import template

register = template.Library()


@register.simple_tag
def render_bundle(_bundle_name, *_args, **_kwargs):
    return ''
