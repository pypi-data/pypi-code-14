import requests
import base64


def twitter_session(config):
    api_key = config['twitter_oauth']['consumer_key']
    api_secret = config['twitter_oauth']['consumer_secret']
    url = config['twitter_api']['auth_api_url']

    session = requests.Session()
    secret = '{}:{}'.format(api_key, api_secret)
    secret64 = base64.b64encode(secret.encode('ascii')).decode('ascii')

    headers = {
        'Authorization': 'Basic {}'.format(secret64),
        'Host': 'api.twitter.com',
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
