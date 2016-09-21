import urllib2
import urllib
import json


def dingtalk_bot(token, post_string, at_mobiles=None):
    data = {
        'msgtype': 'text', 'text': {'content': '%s' % post_string},"at": {"atMobiles": at_mobiles,"isAtAll": 'false'}
    }
    json_str = json.dumps(data)
    req = urllib2.Request(
        "https://oapi.dingtalk.com/robot/send?access_token=%s" % token, json_str)
    req.add_header('Content-type', 'application/json')
    response = urllib2.urlopen(req, timeout=120)
    return response.read()