from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class OpenCredConfig(AppConfig):
    name = 'opencred'
    verbose_name = _('OpenCred password reuse identification')

    def ready(self):
        import opencred.signals  # noqa
