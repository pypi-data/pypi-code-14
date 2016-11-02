from ..twitter import twitter_session, load_tweets

_session = None
_config = None


def init(config, provided_session=None):
    global _config, _session
    _config = config
    if provided_session is not None:
        _session = provided_session


def get_session():
    global _session
    if _session is None:
        _session = twitter_session(_config)
    return _session


def get_tweets(query, result_type, since_id=None):
    if result_type not in ['recent', 'mixed', 'popular']:
        result_type = 'recent'
    return load_tweets(get_session(), _config, query, result_type, since_id=since_id)