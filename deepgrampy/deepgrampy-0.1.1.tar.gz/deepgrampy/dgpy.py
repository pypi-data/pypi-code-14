import requests
import json

class Dg:
    """ Deepgram object """
    def __init__(self, userId):
        self.userId = userId
    def search(self, query, P):
        headers = {
            'Content-Type': 'application/json',
        }
        data = '{ "action": "group_search", "userID": "' + self.userId + '", "tag": "*", "query": "'+ query +'", "filter": {"Nmax": 100000, "Pmin": '+ str(P) +' }, "sort": "time" }'

        r = requests.post('http://groupsearch.api.deepgram.com', headers=headers, data=data)
        responseObject = json.loads(r.text)
        return responseObject['contentID']

    def andSearch(self, queries, Ps):
        allResults = []
        andResults = []
        for i in range(len(queries)):
            allResults.append(self.search(queries[i],Ps[i]))
        for resultSet in allResults:
            for j in resultSet:
                resultTempTrue = []
                if resultSet.index(j)+1 < len(resultSet):
                    for k in allResults:
                        if allResults.index(k)+1 < len(allResults):
                            if j in set(allResults[allResults.index(k)+1]):
                                resultTempTrue.append(True)
                            else:
                                resultTempTrue.append(False)
                    if False not in resultTempTrue:
                        andResults.append(j)
        return set(andResults)

    def orSearch(self, queries, Ps):
        allResults = []
        orResults = []
        for i in range(len(queries)):
            allResults.append(self.search(queries[i],Ps[i]))
        for resultSet in allResults:
            for result in resultSet:
                orResults.append(result)
        return set(orResults)

    def getBalance(self):
        headers = {
            'Content-Type': 'application/json',
        }
        data = '{ "action": "get_balance", "userID": "' + self.userId + '"}'

        r = requests.post('http://api.deepgram.com', headers=headers, data=data)
        responseObject = json.loads(r.text)
        return responseObject["balance"]

    def uploadMedia(self,url):
        headers = {
            'Content-Type': 'application/json',
        }
        data = '{ "action": "index_content", "userID": "' + self.userId + '", "data_url" : "'+ url +'"}'

        r = requests.post('http://api.deepgram.com', headers=headers, data=data)
        responseObject = json.loads(r.text)
        return responseObject

    def checkStatus(self,contentID):
        headers = {
            'Content-Type': 'application/json',
        }
        data = '{ "action": "index_content", "userID": "' + self.userId + '", "contentID" : "'+ contentID +'"}'

        r = requests.post('http://api.deepgram.com', headers=headers, data=data)
        responseObject = json.loads(r.text)
        return responseObject

    def objectSearch(self, contentID, query, Nmax = 10, Pmin = 0.4, sort = "time", snippet = True):
        headers = {
            'Content-Type': 'application/json',
        }
        data = '{ "action": "object_search", "userID": "' + self.userId + '", "contentID" : "'+ contentID +'", "query": "' + query + '", "snippet":"'+ str(snippet) +'", "filter" : {"Nmax": "'+ str(Nmax) +'", "Pmin": "' + str(Pmin) + '"}, "sort": "'+ sort +'"}'

        r = requests.post('http://api.deepgram.com', headers=headers, data=data)
        responseObject = json.loads(r.text)
        return responseObject

    def getTranscript(self, contentID):
        headers = {
            'Content-Type': 'application/json',
        }
        data = '{ "action": "get_object_transcript", "userID": "' + self.userId + '", "contentID" : "'+ contentID +'"}'

        r = requests.post('http://api.deepgram.com', headers=headers, data=data)
        responseObject = json.loads(r.text)
        return responseObject
