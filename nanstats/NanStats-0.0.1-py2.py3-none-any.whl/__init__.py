"""

   \ |                __|  |           |        
  .  |   _` |    \  \__ \   _|   _` |   _| (_-< 
 _|\_| \__,_| _| _| ____/ \__| \__,_| \__| ___/ 


Welcome to NanStats. A python adapter for the Nanigans Reporting API. 

Basic Usage:
g
>>> import nanigans
>>> stats = nanigans.facebook.get_stats()
>>> stats.ok
True

Get Facebook data:

>>> stats = nanigans.facebook.get_stats()
>>> stats.ok
True

Get Multichannel data:

>>> stats = nanigans.multichannel.get_stats()
>>> stats.ok
True

Get Publishers data:

>>> stats = nanigans.publisher.get_stats()
>>> stats.ok
True

"""
from nanigans.utils import Credentials, set_default_config, change_site_id, generate_token

auth = Credentials()

if auth.credentials:
    auth.credentials['token'] = generate_token(auth.credentials['username'], 
                                               auth.credentials['password'],
                                               auth.credentials['site'])

from nanigans.api import facebook, multichannel, publishers, events





