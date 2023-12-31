import functools
from collections import defaultdict
from pydantic import BaseModel
from typing import Optional

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import include, path

from .component import HtmxComponent, RenderedComponent


class HtmxComponentsSite:
    def __init__(self, namespace="htmx"):
        self._register = defaultdict(dict)
        self.namespace = namespace

    def count(self):
        return len(self._register)

    def __register(self, fn, scope, name, model: BaseModel = None):
        self._register[scope].setdefault(
            name, HtmxComponent(fn, self.namespace, scope, name, model)
        )

    def scopes_view(self, request):
        return render(
            request,
            "htmx/_scopes.html",
            context={
                "namespace": self.namespace,
                "scopes": self._register.keys(),
            },
        )

    def scope_view(self, request, scope):
        return render(
            request,
            "htmx/_scope.html",
            context={
                "namespace": self.namespace,
                "scope": scope,
                "components": self._register[scope].values(),
            },
        )

    def render_component(self, request, scope, component, params) -> RenderedComponent:
        components = None
        component_to_render: Optional[HtmxComponent] = None
        try:
            components = self._register[scope]
        except KeyError:
            raise KeyError(
                f"Scope {scope} not found, available scopes: {self._register.keys()}"
            )

        try:
            component_to_render = components[component]
        except KeyError:
            raise KeyError(
                f"Component {component} not found, available components: {', '.join(components.keys())}"
            )
        if component_to_render is None:
            raise KeyError(f"Component {component} not found")
        return component_to_render.render(request, params)

    # todo: static method
    def component_response(self, request, scope, component):
        # TODO: other methods
        params = request.POST.dict() if request.method == "POST" else request.GET.dict()
        component = self.render_component(request, scope, component, params)
        response = HttpResponse(component.content)
        if component.meta is not None:
            if component.meta.event is not None:
                response["HX-Trigger"] = component.meta.event
            if component.meta.full_refresh:
                response["HX-Refresh"] = "true"
        return response

    @property
    def patterns(self):
        return            [
                path("scopes/", self.scopes_view, name="scopes"),
                path("scopes/<str:scope>/", self.scope_view, name="scope"),
                path(
                    "<str:scope>/<str:component>/",
                    self.component_response,
                    name="component",
                ),
            ]


    def get_urls(self):
        return [path(f"{self.namespace}/", include(self.patterns))]

    @property
    def urls(self):
        return self.get_urls(), "htmx", 'htmx'
    def register(self, *, scope: str, name: str, paramsModel: BaseModel = None):
        def decorator(fn):
            @functools.wraps(fn)
            def wrapper(*args, **kwargs):
                return fn(*args, **kwargs)

            self.__register(wrapper, scope, name, paramsModel)
            return wrapper

        return decorator
