from typing import Callable, Optional

from django.http import HttpRequest
from pydantic import BaseModel
from django.template.loader import render_to_string
from django.urls import reverse_lazy

from django_htmx_components.types import ComponentContext, RenderedComponent


class HtmxComponent:
    def __init__(
        self,
        fn: Callable[[HttpRequest, ...], ComponentContext],
        namespace: str,
        scope: str,
        name: str,
        model: Optional[BaseModel] = None,
    ):

        self.fn = fn
        self.template_name = "/".join([namespace, scope, name]) + ".html"
        self.name = name
        self.url = reverse_lazy(
            "htmx:component", kwargs={"scope": scope, "component": name}
        )
        self.model = model

    def render(self, request: HttpRequest, params: dict):
        parsed_params = {}
        if self.model:
            parsed_params = self.model(**params)
        context = self.fn(request, parsed_params)
        return RenderedComponent(
            render_to_string(
                self.template_name, context={**context.params, **{"self_url": self.url}}
            ),
            context.trigger,
        )
