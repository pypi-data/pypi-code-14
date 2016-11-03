from tapioca import TapiocaAdapter, generate_wrapper_from_adapter, JSONAdapterMixin

from requests.auth import HTTPBasicAuth

from .resource_mapping import RESOURCE_MAPPING


class CircleCIClientAdapter(JSONAdapterMixin, TapiocaAdapter):
    api_root = 'https://circleci.com/api/v1.1/'
    resource_mapping = RESOURCE_MAPPING
    _default_resource_kwargs = {'vcs_type': 'github', 'branch': 'master'}

    def get_request_kwargs(self, api_params, *args, **kwargs):
        params = super().get_request_kwargs(api_params, *args, **kwargs)
        params['auth'] = HTTPBasicAuth(api_params.get('token'), '')
        params['headers']['Content-Type'] = 'application/json;charset=UTF-8'
        params['timeout'] = api_params.get('timeout', kwargs.get('timeout', 5))
        return params

    def fill_resource_template_url(self, template, params):
        for key in self._default_resource_kwargs:
            if key in template and key not in params:
                params[key] = self._default_resource_kwargs[key]

        return super().fill_resource_template_url(template, params)


CircleCI = generate_wrapper_from_adapter(CircleCIClientAdapter)
