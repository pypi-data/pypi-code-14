from django_cradmin import javascriptregistry
from ievv_opensource import ievv_jsbase


class IevvJsBaseCoreComponent(javascriptregistry.component.AbstractJsComponent):
    @classmethod
    def get_component_id(cls):
        return 'ievv_jsbase_core'

    def _get_version(self):
        return ievv_jsbase.__version__

    def _versioned_static_urls(self, path_patterns):
        return [
            self.get_static_url(path.format(version=self._get_version()))
            for path in path_patterns
        ]

    def get_sourceurls(self):
        return self._versioned_static_urls([
            'ievv_jsbase/{version}/scripts/ievv_jsbase_core.js'
        ])
