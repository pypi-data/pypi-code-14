import copy
import requests

class sentiments(object):

    def __init__(self):
        self.url = "http://fricles.com:8080/fricles/api/v1/get_sentiments"
        return
    
    def get_sentiments(self, text):
        try:
            r = requests.post(self.url, data={'text':text})
            print r.status_code
            print r.text
        except Exception, err:
            return {"status" : "Failed", "http_code" : err.code, "message" : err.message}
