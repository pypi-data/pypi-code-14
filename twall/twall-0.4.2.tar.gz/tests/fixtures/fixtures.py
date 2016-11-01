import base64

import pytest
import betamax
import os
import configparser
import requests
from betamax_serializers import pretty_json
from betamax.cassette import cassette


def sanitize_token(interaction, current_cassette):
    # This uses a non-public API and still doesn't work to obscure the token in the gzipped response data
    # to the token request. I am aware of the issue but unwilling to spend four hours working around it.

    if 'token' in interaction.data['request']['uri']:
        token = interaction.deserialize().json()['access_token']
        if token is None:
            return

        interaction.replace(token, '<AUTH_TOKEN>')
        current_cassette.placeholders.append(
            cassette.Placeholder(placeholder='<AUTH_TOKEN>', replace=token)
        )


@pytest.fixture
def config():
    cfg = configparser.ConfigParser()
    auth_file_path = os.environ['AUTH_FILE'] if 'AUTH_FILE' in os.environ else 'auth.cfg.default'
    cfg.read(['twall/settings.cfg', auth_file_path])
    return cfg


@pytest.fixture
def betamax_recorder(config):
    with betamax.Betamax.configure() as betamax_config:
        if 'AUTH_FILE' in os.environ:
            betamax_config.default_cassette_options['record_mode'] = 'all'
        else:
            betamax_config.default_cassette_options['record_mode'] = 'none'

        betamax_config.cassette_library_dir = 'tests/fixtures/cassettes'
        betamax_config.before_record(callback=sanitize_token)

        # Sanitize authorization data
        api_key = config['twitter_oauth']['consumer_key']
        api_secret = config['twitter_oauth']['consumer_secret']
        secret = '{}:{}'.format(api_key, api_secret)
        secret64 = base64.b64encode(secret.encode('ascii')).decode('ascii')
        betamax_config.define_cassette_placeholder('<TOKEN>', secret64)

    session = requests.Session()
    betamax.Betamax.register_serializer(pretty_json.PrettyJSONSerializer)
    recorder = betamax.Betamax(session)

    return recorder


@pytest.fixture
def betamax_session_generator(betamax_recorder):
    def make_betamax_session(cassette_name):
        with betamax_recorder.use_cassette(cassette_name, serialize_with='prettyjson'):
            yield betamax_recorder.session

    return make_betamax_session