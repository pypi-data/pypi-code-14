"""
Includes functions for communicating directly with the Twitter API.
"""

import requests
import base64


def twitter_session(config, session=requests.Session()):
    """
    Initializes a new session with the Twitter API. This process includes obtaining a Bearer token using OAuth.

    :param config: A :mod:`configparser` instance containing the application's loaded config data. Must contain Twitter OAuth credentials.
    :param session: If provided, will use this session instead of creating a new one. Useful for testing.
    :return: A :mod:`requests` session containing all the necessary authorization data to communicate with the Twitter Search API.
    """
    api_key = config['twitter_oauth']['consumer_key']
    api_secret = config['twitter_oauth']['consumer_secret']
    url = config['twitter_api']['auth_api_url']

    secret = '{}:{}'.format(api_key, api_secret)
    secret64 = base64.b64encode(secret.encode('ascii')).decode('ascii')

    headers = {
        'Authorization': 'Basic {}'.format(secret64),
        'Host': 'api.twitter.com'
    }

    r = session.post(url,
                     headers=headers,
                     data={'grant_type': 'client_credentials'})

    bearer_token = r.json()['access_token']

    def bearer_auth(req):
        req.headers['Authorization'] = 'Bearer ' + bearer_token
        return req

    session.auth = bearer_auth
    return session


def load_tweets(session, config, query, result_type, count=100, since_id=None):
    """
    Requests tweets from the Twitter Search API. Excludes retweets from the results.

    :param session: A :mod:`requests` session initialized to use the correct Bearer token.
    :param config: A :mod:`configparser` instance containing the application's loaded config data.
    :param query: The search query.
    :param result_type: One of ``recent``, ``mixed`` or ``popular``, specifying which type of tweets should be returned.
    :param count: The maximum number of tweets to return. Note that the actual number of loaded tweets will usually be lower.
    :param since_id: Limits the search to tweets more recent than the tweet with this ID.
    :return: A list of tweet objects retrieved from Twitter.
    """
    if count is None:
        count = 100

    query += '-filter:retweets'
    url = config['twitter_api']['tweet_api_url']
    params = {
        'q': query,
        'result_type': result_type,
        'count': count
    }

    if since_id is not None:
        params['since_id'] = since_id

    response = session.get(url, params=params)
    return response.json()['statuses']
