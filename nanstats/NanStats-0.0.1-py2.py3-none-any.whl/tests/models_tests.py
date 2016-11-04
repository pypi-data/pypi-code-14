import unittest

from mock import Mock, MagicMock, patch
from nanigans.utils import set_default_config
from nanigans.object import Credentials
from nanigans.models import PreparedRequest, Adapter, Response


class RequestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo_string = 'foo'
        cls.foo_dict = {'foo': 'foo'}
        cls.foo_list = ['foo']
        cls.bar_dict = {'bar':'bar'}

    def test_request_requires_resource_to_be_passed_when_instantiating(self):
        with self.assertRaises(TypeError):
            PreparedRequest()
        PreparedRequest(resource=self.foo_string, required_fields=self.bar_dict)

    def test_request_has_necessary_attributes(self):
        request = PreparedRequest(resource='foo', required_fields=self.bar_dict)
        self.assertTrue(hasattr(request, 'resource'))
        self.assertTrue(hasattr(request, 'required_fields'))
        self.assertTrue(hasattr(request, 'parameters'))
        self.assertTrue(hasattr(request, 'send'))

    def test_request_assigns_attributes_correctly_on_instantiation(self):
        request = PreparedRequest(
            resource=self.foo_string, 
            required_fields=self.bar_dict, 
            parameters=self.foo_dict
        )
        self.assertEquals(self.foo_string, request.resource)
        self.assertEquals(self.bar_dict, request.required_fields)
        self.assertEquals(self.foo_dict, request.parameters)

    def test_request_assigns_attributes_correctly_after_instantiation(self):
        request = PreparedRequest(resource='bar', required_fields={'source':'Nanigans'})

        request.resource = self.foo_string
        self.assertEquals(self.foo_string, request.resource)

        request.required_fields = self.bar_dict
        self.assertEquals(self.bar_dict, request.required_fields)

        request.parameters = self.foo_dict
        self.assertEquals(self.foo_dict, request.parameters)

    def test_request_raises_type_error_if_arguments_are_wrong_type(self):
        for non_string in [1, [1], {1}, {'1': 1}, (1, 1)]:
            with self.assertRaises(TypeError):
                PreparedRequest(resource=non_string, required_fields=self.bar_dict)

            request = PreparedRequest(resource='foo', required_fields=self.bar_dict)
            with self.assertRaises(TypeError):
                request.resource = non_string

        for non_dict in [1, [1], {1}, '1', (1, 1)]:
            with self.assertRaises(TypeError):
                PreparedRequest(resource='str', required_fields=non_dict)

            with self.assertRaises(TypeError):
                PreparedRequest(resource='str', required_fields=self.bar_dict, parameters=non_dict)

            request = PreparedRequest(resource='foo', required_fields=self.foo_dict)
            with self.assertRaises(TypeError):
                request.required_fields= non_dict

            request = PreparedRequest(resource='foo', required_fields=self.bar_dict, parameters=self.foo_dict)
            with self.assertRaises(TypeError):
                request.parameters = non_dict

    @patch.object(PreparedRequest, 'send', return_value=None)
    def test_send_method_calls_adapter_get_method(self, mock_request):
        request = PreparedRequest(resource=self.foo_string, required_fields=self.bar_dict)
        request.send()
        mock_request.assert_called_once_with()

    @patch.object(PreparedRequest, 'send', return_value=Response())
    def test_send_method_returns_response_object(self, mock_request):
        request = PreparedRequest(resource=self.foo_string, required_fields=self.bar_dict)
        test_response = request.send()
        self.assertIsInstance(test_response, Response)

    def test_repr_outputs_as_intended(self):
        request = PreparedRequest(resource=self.foo_string, required_fields=self.bar_dict)
        self.assertEquals('<Nanigans Prepared Request [foo]>', repr(request))

        request = PreparedRequest(resource='bar', required_fields=self.bar_dict)
        self.assertEquals('<Nanigans Prepared Request [bar]>', repr(request))

    def test_parameters_default_to_empty_dict(self):
        request = PreparedRequest(resource=self.foo_string, required_fields=self.bar_dict)
        self.assertEquals({}, request.parameters)

        # Ensure that the dictionary used is different across different instances of
        # PreparedRequest.
        another_request = PreparedRequest(resource=self.foo_string, required_fields=self.bar_dict)
        self.assertNotEqual(id(request.parameters),
                            id(another_request.parameters))


class AdapterTests(unittest.TestCase):
    def setUp(self):
        # We mock the Request class so that, if Request changes, we have an
        # obvious starting point from which to make changes to the Adapter
        # class.
        request = Mock()
        request.resource = 'datasources'
        request.api = 'reporting api'
        request.required_fields = {'source':'TestResource'}
        request.parameters = {}
        self.accounts_adapter = Adapter(PreparedRequest=request)

    def test_adapter_requires_request_to_be_passed_when_instantiating(self):
        with self.assertRaises(TypeError):
            Adapter()

    def test_request_has_necessary_attributes(self):
        self.assertTrue(hasattr(self.accounts_adapter, 'request'))
        self.assertTrue(hasattr(self.accounts_adapter, 'endpoint'))
        self.assertTrue(hasattr(self.accounts_adapter, 'params'))
        self.assertTrue(hasattr(self.accounts_adapter, 'get'))

    def test_endpoint_attribute_returns_str(self):
        self.assertIsInstance(self.accounts_adapter.endpoint, str)

    def test_unknown_resource_raises_type_error_when_getting_endpoint(self):
        request = MagicMock()
        request.resource = 'invalid'
        adapter = Adapter(PreparedRequest=request)
        with self.assertRaises(TypeError):
            adapter.endpoint

    def test_params_returns_specific_dictionary_if_no_optional_params_in_request(self):
        self.assertIn('access_token', self.accounts_adapter.params.keys())
        self.assertIn('format', self.accounts_adapter.params.keys())

    def test_params_returns_params_if_in_request(self):
        request = Mock()
        request.resource = 'accounts'
        request.parameters = {'foo':'bar', 'bar':'baz'}
        adapter = Adapter(PreparedRequest=request)
        self.assertEquals(request.parameters, adapter.params)

    def test_get_calls(self):
        resp = MagicMock()
        resp.json = Mock()
        resp.status_code = Mock()
        with patch.object(Adapter, 'get', return_value=resp) as get_request:
            self.accounts_adapter.get()

        get_request.assert_any_call()

    @patch('nanigans.models.Adapter.get')
    def test_send_returns_response_with_errors_if_errors(self, mock_get):

        errors = [{'code': 'foo'}]
        resp = Response(data=[], errors=errors)

        mock_get.status_code = 403
        mock_get.return_value = resp
        response = self.accounts_adapter.get()

        self.assertIsInstance(response, Response)
        self.assertEquals(errors, response.errors)
        self.assertEquals([], response.data)

    def test_repr_outputs_as_intended(self):
        self.assertEquals('<Nanigans Adapter [Reporting API]>', repr(self.accounts_adapter))


class ResponseTests(unittest.TestCase):
    def test_response_can_be_instantiated_with_no_arguments(self):
        Response()

    def test_response_has_necessary_attributes(self):
        response = Response()
        self.assertTrue(hasattr(response, 'data'))
        self.assertTrue(hasattr(response, 'errors'))
        self.assertTrue(hasattr(response, 'ok'))

    def test_response_can_be_instantiated_with_data_only(self):
        Response(data=None)
        Response(data=[])
        Response(data=[1])

    def test_response_can_be_instantiated_with_errors_only(self):
        Response(errors=None)
        Response(errors=[])
        Response(errors=[1])

    def test_response_raises_if_instantiated_with_non_lists(self):
        for non_list in [1, '1', {1}, {'1': 1}, (1, 1)]:
            with self.assertRaises(TypeError):
                Response(data=non_list)
            with self.assertRaises(TypeError):
                Response(errors=non_list)

    def test_data_is_assigned_to_attribute_if_not_none(self):
        data = [1, 2, 3]
        response = Response(data=data)
        self.assertEquals(data, response.data)

    def test_data_attribute_is_empty_list_if_data_is_none(self):
        self.assertEquals([], Response().data)

    def test_errors_is_assigned_to_attribute_if_not_none(self):
        errors = [4, 5, 6]
        response = Response(errors=errors)
        self.assertEquals(errors, response.errors)

    def test_errors_attribute_is_empty_list_if_errors_is_none(self):
        self.assertEquals([], Response().errors)

    def test_ok_returns_true_if_errors_is_empty(self):
        response = Response(data=[1, 2, 3], errors=None)
        self.assertTrue(response.ok)

        response = Response(data=None, errors=None)
        self.assertTrue(response.ok)

    def test_ok_returns_false_if_errors_not_empty(self):
        response = Response(data=[1, 2, 3], errors=[1, 2, 3])
        self.assertFalse(response.ok)

        response = Response(data=None, errors=[1, 2, 3])
        self.assertFalse(response.ok)

    def test_bool_returns_true_if_errors_is_empty(self):
        response = Response(data=[1, 2, 3], errors=None)
        self.assertTrue(response)

        response = Response(data=None, errors=None)
        self.assertTrue(response)

    def test_bool_returns_false_if_errors_not_empty(self):
        response = Response(data=[1, 2, 3], errors=[1, 2, 3])
        self.assertFalse(response)

        response = Response(data=None, errors=[1, 2, 3])
        self.assertFalse(response)

    def test_empty_response_is_added_to_non_empty_response_correctly(self):
        data_a = [1]
        errors_a = ['a']
        response_a = Response(data=data_a, errors=errors_a)
        response_b = Response()

        response_sum = response_a + response_b
        self.assertEquals(data_a, response_sum.data)
        self.assertEquals(errors_a, response_sum.errors)

    def test_non_empty_responses_are_added_correctly(self):
        data_a = [1]
        errors_a = ['a']
        response_a = Response(data=data_a, errors=errors_a)

        data_b = [2]
        errors_b = ['b']
        response_b = Response(data=data_b, errors=errors_b)

        response_sum = response_a + response_b
        self.assertEquals(data_a + data_b, response_sum.data)
        self.assertEquals(errors_a + errors_b, response_sum.errors)

    def test_adding_non_response_to_response_raises_type_error(self):
        response = Response()
        for non_response in [1, '1', {1}, {'1': 1}, (1, 1), [1]]:
            with self.assertRaises(TypeError):
                response + non_response

    def test_repr_outputs_as_intended(self):
        response = Response(data=[1])
        self.assertEquals('<Nanigans Response [OK]>', repr(response))

        response = Response(errors=[1])
        self.assertEquals('<Nanigans Response [Incomplete]>', repr(response))


if __name__ == "__main__":
    
    test_user = 'username@fakers.com'
    test_password = 'fakePass5000'
    test_site = 123456
    auth = Credentials()
    set_default_config(test_user, test_password, test_site)

    test_cases = [RequestTests, AdapterTests, ResponseTests]

    for test_case in test_cases:
        suite = unittest.TestLoader().loadTestsFromTestCase(test_case)
        unittest.TextTestRunner(verbosity=1).run(suite)
