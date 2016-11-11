import pandas as pd
import tweepy
from somecode import data_frame

def search(query,max_tweets=200,language='en'):

    access_token = "731718844264251392-n4NiVuKrDyCRNSVttgl9KM7QgUy9Gcx"
    access_secret = "NxGnlIa08eVgbuyh5sznphCGHuMQ3A8ES1jO2YqFIJ1zA"
    consumer_secret = "nlUQLufKwWyEHJRyVWVi3gOJ0IPIv7WtaQewQf02LFzxE7lZYn"
    consumer_key = "hhOHS09gS3blQhXK0atmdTGtw"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth,wait_on_rate_limit=True)

    ## THE LANGUAGE IS CURRENT HARD CODED (have to remove soon)

    #language = "fi"

    searched_tweets = []
    last_id = -1

    while len(searched_tweets) < max_tweets:

        count = max_tweets - len(searched_tweets)

        try:
            new_tweets = api.search(q=query, count=count, max_id=str(last_id - 1), lang=language)

            if not new_tweets:
                break

            searched_tweets.extend(new_tweets)
            last_id = new_tweets[-1].id

        except tweepy.TweepError as e:
            break
    print "\n" + "DataFrame with n=" + str(max_tweets) + " for keyword \'" + str(query) + "\' created on " + str(pd.to_datetime('now')) + " succesfully withour errors." + "\n"
    
    df = data_frame(searched_tweets)
    df.meta_keyword = str(query)

    return df