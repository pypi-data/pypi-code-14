""" Module provides sentiment for the given text.

        >> How to install ?
            pip install fricles

        >> How to use ?
            from fricles import sentiments
        sent_op = sentiments().get_sentiments("text")
@author: Chetan G
@contact: chetan.ganjihal@gmail.com
@since: Created on 2016-02-04
@copyright: Copyright (C) 2016 Chetan Team. All rights reserved.
@license: http://www.apache.org/licenses/LICENSE-2.0 Apache License
"""

#'

import copy
import requests

class sentiments:

    url = "http://fricles.com:8080/fricles/api/v1/get_sentiments"
    data = { "text" : "hello world" } 
    def get_sentiments(self, text):
        inputData = copy.deepcopy(self.data.copy())
        try:
            print "Sentiments for ", inputData
            r = requests.post(self.url, data=inputData)
            print r.status_code
            print r.text
        except Exception, err:
            return {"status" : "Failed", "http_code" : err.code, "message" : err.message}

