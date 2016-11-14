#!/usr/local/bin/python3


import time

import requests


def sendPush(userkey, appkey, message, *, device='', title='', url='', url_title='', priority='', timestamp='', sound=''):
    '''Send a push notification via Pushover.net

    Parameters: look at 'https://pushover.net/api'
        you may need to use time.gmtime(), time.localtime(), time.mktime(), or calendar.timegm() for timestamp.
    Return: response status code.
    '''

    payload = {
        'token': appkey, 
        'user': userkey, 
        'message': message, 
    }

    if device != '':
        payload['device'] = device
    if title != '':
        payload['title'] = title
    if url != '':
        payload['url'] = url
    if url_title != '':
        payload['url_title'] = url_title
    if priority != '':
        priority = int(priority)
        if priority in [-2, -1, 1, 2]:
            payload['priority'] = str(priority)
        else:
            return None
    if timestamp != '':
        timestamp = int(float(timestamp))
        payload['timestamp'] = str(timestamp)
    if sound != '':
        payload['sound'] = sound

    noti_response = requests.post('https://api.pushover.net/1/messages.json', data=payload)
    return noti_response.status_code
