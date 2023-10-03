# In a file called [project root]/components/calendar/calendar.py
from django_components import component

from django_htmx_components import (
    ComponentContext,
    ComponentWithHtmx,
    expose_as_htmx_component,
    htmx_component,
)


@component.register("calendar")
class Calendar(component.Component):
    # Templates inside `[your apps]/components` dir and `[project root]/components` dir will be automatically found. To customize which template to use based on context
    # you can override def get_template_name() instead of specifying the below variable.
    template_name = "calendar/calendar.html"

    # This component takes one parameter, a date string to show in the template
    def get_context_data(self, date):
        return {
            "date": date,
        }
