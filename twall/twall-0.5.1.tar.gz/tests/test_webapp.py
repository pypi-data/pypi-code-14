from tests.fixtures.fixtures import config, betamax_recorder, betamax_session_generator
import pytest
from twall.web import create_app_with_config
from twall.twitter import twitter_session


@pytest.yield_fixture()
def betamax_session(betamax_session_generator):
    for s in betamax_session_generator('webapp_cassette'):
        yield s


@pytest.fixture
def webapp_client(config, betamax_session):
    session = twitter_session(config, betamax_session)
    app = create_app_with_config(config, twitter_session=session)
    app.config['TESTING'] = True
    return app.test_client()


def test_load_homepage(webapp_client):
    data = webapp_client.get('/').data.decode('utf-8')
    assert 'Twitter Wall' in data
    assert 'id="search-field"' in data
    assert '"twitter-tweet"' not in data


@pytest.mark.parametrize('query', ['#trump', 'python'])
@pytest.mark.parametrize('mode', ['recent', 'mixed', 'popular', 'badmode'])
def test_search_tweets(webapp_client, query, mode):
    data = webapp_client.get('/?q=' + query + '&mode=' + mode).data.decode('utf-8')
    assert 'Twitter Wall' in data
    assert 'id="search-field"' in data
    assert 'value="' + query + '"' in data

    # Even in popular mode, we should be getting at least 5 tweets
    assert data.count('"twitter-tweet"') >= 5

    # Testing that links to hashtags appear in the response
    if '#' in query:
        assert '<a href="https://twitter.com/hashtag/{}" target="_blank">{}</a>'.format(query[1:], query) in data