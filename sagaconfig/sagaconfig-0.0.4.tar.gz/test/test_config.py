import unittest


class TestConfig(unittest.TestCase):

    def test_config(self):
        from src import config
        assert(config == dict())

    def test_config_merge(self):
        one = {
            'only_in_1': True,
            'nested': {
                'only_in_1': True,
                'conflicting': False
            },
            'conflicting': False
        }
        two = {
            'only_in_2': True,
            'nested': {
                'only_in_2': True,
                'conflicting': True
            },
            'conflicting': True
        }
        from src import merge_configs
        merged = merge_configs(one, two)
        assert(merged['only_in_1'])
        assert(merged['only_in_2'])
        assert(merged['conflicting'])
        assert(merged['nested']['only_in_1'])
        assert(merged['nested']['only_in_2'])
        assert(merged['nested']['conflicting'])

    def test_bad_config_merge(self):
        one = {
            'nested': 'string'
        }
        two = {
            'nested': {
                'only_in_2': True,
                'conflicting': True
            }
        }
        from src import merge_configs
        merged = merge_configs(one, two)
        assert(merged['nested']['only_in_2'])
        assert(merged['nested']['conflicting'])

    def test_load_config(self):
        from src import load_config
        example_config = load_config('example_config')
        assert(example_config['default_string'] == 'string')
