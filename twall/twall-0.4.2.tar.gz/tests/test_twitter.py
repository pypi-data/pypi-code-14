from twall.twitter import twitter_session, load_tweets
from tests.fixtures.fixtures import config, betamax_recorder, betamax_session_generator
import pytest


@pytest.yield_fixture()
def betamax_session(betamax_session_generator):
    for s in betamax_session_generator('twitter_cassette'):
        yield s


@pytest.mark.parametrize(['count', 'query'],
                         [(None, 'python'),
                          (10, 'ruby'),
                          (20, '#java'),
                          (50, '#swift')])
def test_load_tweets(config, betamax_session, count, query):
    session = twitter_session(config, session=betamax_session)
    tweets = load_tweets(session, config, query, 'recent', count=count)
    expected_count = count if count is not None else 100

    # Twitter sometimes returns fewer tweets than we want but the value should be at least half
    assert len(tweets) >= expected_count / 2
    contains = 0
    for tw in tweets:
        if query in tw['text'].lower() or query in tw['user']['screen_name'].lower():
            contains += 1

    # At least half of the tweets should contain the query in their text or user's screen name
    assert contains > len(tweets) / 2


def test_load_since_id(config, betamax_session):
    session = twitter_session(config, session=betamax_session)
    tweets = load_tweets(session, config, '#python', 'recent')
    max_tweet_id = max(tweets, key=lambda t: t['id'])['id']
    tweets = load_tweets(session, config, '#python', 'recent', since_id=max_tweet_id)
    assert all([t['id'] > max_tweet_id for t in tweets])
