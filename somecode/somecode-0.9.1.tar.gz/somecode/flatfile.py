import pandas as pd
from data_frame import data_frame
from data_prep import data_prep

def flatfile(filename='somecode_tweets.json'):
    
    with open(filename, 'rb') as f:

        data = f.readlines()

        data = map(lambda x: x.rstrip(), data)
        data_json_str = "[" + ','.join(data) + "]"
        data_df = pd.read_json(data_json_str)
        t = data_df[data_df['user'].isnull() != True]
        t = pd.DataFrame.reset_index(t)
        
    t.drop(['coordinates','display_text_range','display_text_range','geo',
         'extended_entities','timestamp_ms','source','quoted_status_id_str',
         'quoted_status','place','is_quote_status','in_reply_to_user_id',
         'in_reply_to_status_id','id_str','favorited','extended_tweet',
         'entities','contributors','truncated','retweeted_status','quoted_status_id',
         'in_reply_to_user_id_str','in_reply_to_status_id_str','in_reply_to_screen_name',
         'filter_level'], axis=1, inplace=True)

    df = data_frame(data_prep(t))
    
    return df