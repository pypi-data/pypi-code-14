from django.apps import AppConfig


class BibblioConfig(AppConfig):
    name = 'bibblio'
    verbose_name = "Bibblio"

    def ready(self):
        from .registration import autodiscover
        autodiscover()
