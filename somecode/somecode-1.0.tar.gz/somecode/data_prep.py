import pandas as pd

def data_prep(data):
    
    """
    It will take about 15 seconds for 30,000 tweet objects 
    when read from a .json file in the full format
    
    """
    
    r = int(len(data))

    test = [[data['user'][i]['statuses_count'],
            data['user'][i]['followers_count'],
            data['user'][i]['friends_count'],
            data['user'][i]['listed_count'],
            data['user'][i]['favourites_count'],
            data['user'][i]['screen_name'],    
            data['user'][i]['created_at'],
            data['user'][i]['default_profile'],
            data['user'][i]['default_profile_image'],
            data['user'][i]['location'],
            data['user'][i]['time_zone'],
            data['user'][i]['name'],      
            data['user'][i]['lang'],
            data['user'][i]['description'],
            data['user'][i]['url'],
            data['user'][i]['verified']] for i in range(r)] 

    df1 = pd.DataFrame(test)
    
    df1.columns = ['user.statuses_count',
                   'user.followers_count',
                   'user.friends_count',
                   'user.listed_count',
                   'user.favourites_count',
                   'user.screen_name',
                   'user.created_at',
                   'user.default_profile',
                   'user.default_profile_image',
                   'user.location',
                   'user.time_zone',
                   'user.name',
                   'user.lang',
                   'user.description',
                   'user.url',
                   'user.verified']
    
    out = pd.concat([df1,data], axis=1)
    
    return out