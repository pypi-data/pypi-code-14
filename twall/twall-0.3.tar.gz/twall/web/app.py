from flask import Flask, Blueprint, render_template, request, Markup
import configparser
from . import twitter_adapter
import os


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

blueprint = Blueprint('app', __name__)


def create_app(auth_filename, debug=False):
    app = Flask(__name__)
    app.debug = debug
    config = configparser.ConfigParser()
    config.read([auth_filename, os.path.join(__location__, '../settings.cfg')])
    twitter_adapter.init(config)

    app.register_blueprint(blueprint)

    app.jinja_env.filters['render_image'] = render_media
    app.jinja_env.filters['render_tweet'] = render_tweet

    return app


@blueprint.route('/')
def wall():
    ctx = {}
    query = request.args.get('q')
    if query is not None:
        result_type = request.args.get('mode').lower()
        ctx['mode'] = result_type
        ctx['query'] = query
        ctx['tweets'] = twitter_adapter.get_tweets(query, result_type=result_type)
    else:
        ctx['mode'] = 'recent'

    return render_template('wall.html', **ctx)


def render_hashtag(hashtag, text):
    return '<a href="https://twitter.com/hashtag/{}" target="_blank">{}</a>'.format(hashtag, text)


def render_mention(screen_name, text):
    return '<a href="https://twitter.com/{}" target="_blank">{}</a>'.format(screen_name, text)


def render_link(url, text):
    return '<a href="{}" target="_blank">{}</a>'.format(url, text)


def render_media(media):
    width = min(400, media['sizes']['medium']['w'])
    height = width * (media['sizes']['medium']['h'] / media['sizes']['medium']['w'])
    return Markup('<img src="{}" width="{}" height="{}"/>'.format(media['media_url'], width, height))


def render_tweet(tweet):
    new_text = tweet['text']

    for mention in tweet['entities']['user_mentions']:
        new_text = enrich_text(tweet['text'], new_text, mention['indices'], mention['screen_name'], render_mention)

    for hashtag in tweet['entities']['hashtags']:
        new_text = enrich_text(tweet['text'], new_text, hashtag['indices'], hashtag['text'], render_hashtag)

    for link in tweet['entities']['urls']:
        new_text = enrich_text(tweet['text'], new_text, link['indices'], link['expanded_url'], render_link)

    return Markup(new_text)


def enrich_text(original_text, constructed_text, indices, entity_info, render_method):
    original_text_chunk = original_text[indices[0]:indices[1]]
    new_text = constructed_text.replace(original_text_chunk, render_method(entity_info,
                                                                           original_text_chunk))
    return new_text
