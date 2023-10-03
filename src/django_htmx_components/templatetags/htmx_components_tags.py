from django import template

from .. import htmx_component as core

register = template.Library()


@register.simple_tag(takes_context=True)
def htmx_component(context, _scope, _name, **params):
    request = context.get("request")
    return core.render_component(request, _scope, _name, params).content
