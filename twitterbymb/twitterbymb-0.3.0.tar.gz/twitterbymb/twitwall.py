import base64
import requests
import click
import time
import configparser
from flask import *
import jinja2
import re
app = Flask(__name__)


@app.route('/')
@app.route('/<hashtag>')
def generate_web(hashtag=None,json_twit=None):
    twit = app.config['twitterobj']
    sess = app.config['session']
    if hashtag:
        json_twit = twit.get_tweet(sess, hashtag, 20, False, 0)

    return render_template('twitter.html',hashtag=hashtag, json_twit=json_twit)

@app.template_filter('hashtag_filter')
def replace_hashtag(tweet_textik):
    tweet_text = re.sub(r'(http[s*]://[^ ]+)', '<a href="\\1">\\1</a>', tweet_textik)
    hashtext = re.sub(r'(\A|\s)#(\w+)', '\\1<a href="http://twitter.com/#\\2">#\\2</a>', tweet_text)
    mentiontext = re.sub(r'(^|[^@\w])@(\w{1,15})\b', '\\1<a href="http://twitter.com/\\2">@\\2</a>', hashtext)

    return jinja2.Markup(mentiontext)

@click.group()
def cmd():
    pass

@cmd.command()
def web():
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    sess = web_main(None)
    app.run(debug=True)

@cmd.command()
@click.option('--num', default=5, help='Number of tweets')
@click.option('--hashtag', prompt='hashtag with #', default='#king' , help='What tweets you wanna see ?!?')
@click.option('--authfile', default='auth.cfg', help='Path to authorization file.')
@click.option('--timeout', default=30, help='Number of secconds for checking new issues.')
@click.option('--nort/--rt', default=False, help='If used no retweets will be shown, by default it is false')
@click.pass_context
def cli(ctx,num,hashtag,authfile,timeout,nort): # **kwargs
    #ctx.obj_['num'] = num
    return ctx

class TwitterWall(object):
    def __init__(self,numOfTweet,hashtag,switch):
        self.numOfTweet=numOfTweet
        self.hashtag=hashtag
        self.switch=switch

    def getMeSession (self,api_key,api_secret):
        session = requests.session()
        secret = '{}:{}'.format(api_key, api_secret)
        secret64 = base64.b64encode(secret.encode('ascii')).decode('ascii')
        headers = {  # what are headers - tony
            'Authorization': 'Basic {}'.format(secret64),
            'Host': 'api.twitter.com',
        }
        r = session.post('https://api.twitter.com/oauth2/token', headers=headers,
                         data={'grant_type': 'client_credentials'})
        r.json()
        bearer_token = r.json()['access_token']
        def bearer_auth(req):
            req.headers['Authorization'] = 'Bearer ' + bearer_token
            return req

        session.auth = bearer_auth
        return session

    def get_tweet(self,session, hashtag, count, rt, since_id):
        q = session.get('https://api.twitter.com/1.1/search/tweets.json', params={'q': hashtag, 'count': count, 'since_id': since_id})
        return q.json()['statuses']

    def print_tweet(self,session, hashtag, count, rt, since_id):
        q = session.get('https://api.twitter.com/1.1/search/tweets.json', params={'q': hashtag, 'count': count, 'since_id': since_id})
        for tweet in q.json()['statuses']:
            if rt:
                if tweet['retweet_count'] == 0:
                    print(tweet['text'])
                    id = tweet['id']
            else:
                print(tweet['text'])
                id = tweet['id']
        return id

def web_main(hashtag):
    config = configparser.ConfigParser()
    config.read('auth.cfg')
    twit = TwitterWall(20,hashtag, False)         
    app.config['twitterobj'] = twit
    app.config['session'] = twit.getMeSession(config['twitter']['api_key'],config['twitter']['api_secret'])

def my_main(ctx):
    config = configparser.ConfigParser()
    config.read(ctx.params['authfile'])
    id = 0
    twit = TwitterWall(ctx.params['num'],ctx.params['hashtag'],ctx.params['nort'])
    session = twit.getMeSession(config['twitter']['api_key'],config['twitter']['api_secret'])
    while(True):
        id = twit.print_tweet(session,twit.hashtag, twit.numOfTweet, twit.switch,id)
        time.sleep(ctx.params['timeout'])



def main():
    context = cmd(standalone_mode=False)
    if context:
        my_main(context)
    #context.obj_ = {}
    #print(context.params['hashtag'])

if __name__ == '__main__':
    main()
