from django.apps import AppConfig
from django.conf import settings
from django.utils.module_loading import autodiscover_modules


class HtmxComponentsConfig(AppConfig):
    name = 'django_htmx_components'

    def ready(self):
        autodiscover_modules('htmx')
        autodiscover_modules('components')

