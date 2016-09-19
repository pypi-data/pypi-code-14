from django.apps import AppConfig

default_app_config = 'leonardo_module_links.LinksConfig'


class Default(object):

    optgroup = ('Link lists')

    apps = [
        'leonardo_module_links',
    ]

    css_files = [
        'css/bootstrap-social.css'
    ]

    @property
    def widgets(self):
        return [
            'leonardo_module_links.widget.models.LinkButtonWidget',
            'leonardo_module_links.widget.models.LinkMenuWidget',
        ]


class LinksConfig(AppConfig, Default):
    name = 'leonardo_module_links'
    verbose_name = "Link lists"

default = Default()
