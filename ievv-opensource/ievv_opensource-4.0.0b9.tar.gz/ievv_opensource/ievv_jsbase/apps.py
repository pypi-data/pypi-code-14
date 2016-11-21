from django.apps import AppConfig
from django_cradmin import javascriptregistry
from ievv_opensource.ievv_jsbase import static_components


class IevvJsBaseAppConfig(AppConfig):
    name = 'ievv_opensource.ievv_jsbase'
    verbose_name = "IEVV jsbase"

    def ready(self):
        javascriptregistry.Registry.get_instance().add(
            static_components.IevvJsBaseCoreComponent)
