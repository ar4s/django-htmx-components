from debug_toolbar.panels import Panel
from django.utils.translation import gettext_lazy as _
from .. import htmx_component

class CustomerPanel(Panel):
    template = "debug_toolbar/panels/registry.html"

    title = _("HTMX Components")

    @property
    def nav_subtitle(self):
        return f"{htmx_component.count()} in register"

    def generate_stats(self, request, response):
        self.record_stats({
            "registry": htmx_component._register.items(),
            "scopes": htmx_component._register.keys()
        })
