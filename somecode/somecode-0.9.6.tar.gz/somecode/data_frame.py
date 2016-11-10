import pandas as pd
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def data_frame(data):

    try:
        nltk.download('vader_lexicon')

    except:
        pass

    try:
        df1 = pd.DataFrame([[tweet.user.statuses_count, 
                             tweet.user.favourites_count, 
                             tweet.user.followers_count, 
                             tweet.user.friends_count, 
                             tweet.user.listed_count] 
                             for tweet in data], 
                             columns=('user_tweets','user_favourites','user_followers',
                                      'user_following','user_listed'))
    except AttributeError:
        df1 = pd.DataFrame({
                            'user_favourites' : data['user.favourites_count'],
                            'user_tweets' : data['user.statuses_count'],
                            'user_followers' : data['user.followers_count'],
                            'user_following' : data['user.friends_count'],
                            'user_listed' : data['user.listed_count']})
        
    try: 
        df2 = pd.DataFrame([[tweet.user.screen_name, pd.to_datetime(tweet.user.created_at),
                        tweet.user.default_profile, tweet.user.default_profile_image, 
                        tweet.user.description, tweet.user.location,
                        tweet.user.time_zone] for tweet in data], 
                        columns=('handle','created_at','default_profile',
                                 'egg_account','description','location','timezone'))
        
    except AttributeError:     
        df2 = pd.DataFrame({
                        'handle' : data['user.screen_name'],
                        'created_at' : pd.to_datetime(data['user.created_at']),
                        'default_profile' : data['user.default_profile'],      
                        'egg_account' : data['user.default_profile_image'], 
                        'description' : data['user.description'],
                        'location' : data['user.location'],
                        'timezone' : data['user.time_zone']})
        
    l = []

    try:
    
        for tweet in data: 
            try:
                l.append(tweet.user.entities['url']['urls'][0]['expanded_url'])
            except KeyError:
                l.append("")   

    except AttributeError:
            
        for tweet in data: 
            try:
                l.append(data['user']['url'])
            except KeyError:
                l.append("")   
           
    #df2['url'] = l
    
    try:
        df3 = pd.DataFrame([[tweet.retweet_count,tweet.text.encode("utf-8")] for tweet in data], columns=('retweet_count','text'))
    except AttributeError:
        df3 = pd.DataFrame({'retweet_count' : data.retweet_count,
                            'text' : data.text.str.encode("utf-8")})
                                                            
    df = pd.concat([df3,df1,df2], axis=1)
    
        ### COUNTING THE LOW QUALITY SCORE
    
    low_quality = pd.DataFrame({'default_profile' : df.default_profile == True,
                                'egg_account' : df.egg_account == True,
                                #'no_bio_url' : df.url == "",
                                'no_description' : df.description == "",
                                'follows_more' : df.user_following > df.user_followers,
                                'spam_account' : df.user_tweets > 50 * df.user_followers,
                                'many_tweets' : df.user_tweets > 50000,
                                'created_2016' : df.created_at.dt.year == 2016,
                                'many_favorites' : df.user_favourites > df.user_tweets,
                                'few_listed' : df.user_listed < df.user_followers / 100})
    
    df4 = pd.DataFrame(10 - low_quality.sum(axis=1)) 
    df4.columns = ['quality_score']
    df = pd.concat([df4,df], axis=1)
    
    ### COUNTING INFLUENCE SCORE 
    
    df5 = pd.DataFrame((pd.to_datetime('today') - df.created_at).dt.days + 2)
    df5.columns = ['days_since_creation']
    
    influence = pd.DataFrame({'listed_per_tweet' : np.log(df.user_listed+1 / df.user_tweets+1),
                                'followers_per_tweet' : np.log(df.user_followers+1 / df.user_tweets+1),
                                'followers_per_day' : np.log(df.user_followers+1 / df5['days_since_creation']+1),
                                'listed_per_day' : np.log(df.user_listed+1 / df5['days_since_creation']+1),
                                'listed_per_follower' : np.log(df.user_listed+1 / df.user_followers+1)})

    df5['influence_score'] = pd.DataFrame(influence.sum(axis=1))
    df5['reach_score'] = df.user_followers / 10 * df5.influence_score + 1     

    df5['influence_score'] = df5.influence_score.replace("inf", 1).fillna(1).astype(int)
    df5['reach_score'] = df5.reach_score.replace("inf", 1).fillna(1).astype(int)

    df = pd.concat([df5,df], axis=1)

    ## SENTIMENT ANALYSIS MODULE

    sid = SentimentIntensityAnalyzer()
    l = []
    l = [np.append(l,sid.polarity_scores(tweet).values()) for tweet in df.text]
    df6 = pd.DataFrame(l,columns=('compound','neu','neg','pos'))

    df = pd.concat([df,df6], axis=1)
    
    df = df.sort_values('retweet_count', ascending=False)
    
    return df