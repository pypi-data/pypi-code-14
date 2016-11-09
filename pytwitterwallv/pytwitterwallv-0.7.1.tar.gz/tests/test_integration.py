import base64
import configparser
import json
import os

import betamax
import pytest
from betamax.cassette.cassette import Placeholder
from flexmock import flexmock

from pytwitterwallv.pytwitterwallv import TwitterWall

with betamax.Betamax.configure() as config:
    config.cassette_library_dir = 'tests/fixtures/cassettes'
    config_file = "./tests/auth.cfg"
    if os.path.isfile(config_file):
        c = configparser.ConfigParser()
        c.read(config_file)
        API_KEY = c['twitter']['key']
        API_SECRET = c['twitter']['secret']
        config.default_cassette_options['record_mode'] = 'all'

        config.define_cassette_placeholder(
            '<AUTH REQ>',
            base64.b64encode('{}:{}'.format(API_KEY, API_SECRET).encode('ascii')).decode('ascii')
        )


        def before_record(interaction, cassette):
            if interaction.data['response']['url'] == 'https://api.twitter.com/oauth2/token':
                placeholder = '{"access_token": "<AUTH RESP>"}'
                data = interaction.data['response']['body']['string']
                cassette.placeholders.append(
                    Placeholder(placeholder=placeholder, replace=data)
                )


        config.before_record(callback=before_record)

    else:
        API_KEY = 'false_api_key'
        API_SECRET = 'false_api_secret'
        config.default_cassette_options['record_mode'] = 'none'


@pytest.fixture
def twitter_client(betamax_session):
    tw = TwitterWall(request_session=betamax_session)
    tw.init_session(API_KEY, API_SECRET)
    return tw


@pytest.fixture
def testapp(twitter_client):
    from pytwitterwallv.pytwitterwallv import app
    app.config['API_KEY'] = "fake_api_key"
    app.config['API_SECRET'] = "fake_api_secret"
    app.config['TESTING'] = True

    app.config["TWITTER_CLIENT"] = twitter_client

    return app.test_client()


def test_twitter_client(twitter_client):
    query = '#python'
    tweets = twitter_client.tweets(query, 1)
    assert len(tweets) >= 0


@pytest.mark.parametrize("hashtag", ("python", "java"))
def test_web(testapp, hashtag):
    resp = testapp.get('/{}/'.format(hashtag)).data.decode('utf-8')
    r = resp.find("<title>#{}</title>".format(hashtag))
    assert r > 0


def test_search_python_with_mock():
    with open("./tests/fixtures/tweets.json") as data_file:
        def mock_generator(query, initial_count, interval):
            data = json.load(data_file)
            return [data]

        tw = TwitterWall()
        flexmock(tw).should_call("display").once()
        tw.infinite_generator = mock_generator
        tw.infinite_printer("#python", 1, 2, True, True)
