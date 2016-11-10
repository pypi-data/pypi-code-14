def key():

    from random import randint
    import pandas as pd
    
    di = {}
    
    x = randint(1,2)

    if x == 1:
        token = "730761128951734273-F6QTnBibFat750m48yu1B6thTqWGtqj"
        token_secret = "b4u10GQurb9bqu7hteukMLdN1IMgbWdaQeHRFmyCEkdAu"
        consumer_secret = "YOFK1er2ErmL1bPLCGPdMvdQ8GNdZT3EVp1zlWWmb550fswajS"
        consumer_key = "PW0loTMtmxIJORhgpVKbAi3O7"

    elif x == 2: 
        token = "730749638228115456-zVgNlOzMhhneUJhwPDLNK8LhQIH7dwJ"
        token_secret = "eb5Ul4Afk6tX4ZHqeLyKEBazc9LdijrrZzkjzCrFie3nO"
        consumer_secret = "72OPxzPfxlod3qZ5gYUFHSetOQT7PzmthCllOGHZbrXWYGzzes"
        consumer_key = "yGD26irzuYOnT3RBB5W8tHqxm"
        
    di.update({'token' : token,
                     'token_secret' : token_secret,
                     'consumer_secret' : consumer_secret,
                     'consumer_key' : consumer_key})    

    return di