from django.apps import AppConfig


class BatchOperationAppConfig(AppConfig):
    name = 'ievv_opensource.ievv_batchframework'
    verbose_name = "IEVV batch operation"

    def ready(self):
        from django_cradmin.superuserui import superuserui_registry
        appconfig = superuserui_registry.default.add_djangoapp(
            superuserui_registry.DjangoAppConfig(app_label='ievv_batchframework'))
        appconfig.add_all_models()
