# oopyconnector : python framework for connecting to the Only Once API
#
#
# Author(s)     :   - Henri Kuiper (henri.kuiper@onlyonce.com)

#
#
# Version       : 2.0beta

import requests
import datetime

import names

def is_paginated(response_json):
    return not response_json['last']

class OOCardParser():
    '''Helper class for parsing of cards
    '''

    def findField(self, field, model):
        '''Finds a field within a card or returns None
        '''
        if model.has_key('definitionName'):
            if model['definitionName'] == field:
                return model['value']
        if model.has_key('components'):
            for item in model['components']:
                val = self.findField(field, item)
                if val != None:
                    return val

    def getInfo(self, model, fields):
        '''Retrieves all fields from a card. Fields should be speicifed as a list of 'strings'.
        '''
        res = {}
        for field in fields:
            res[field] = self.findField(field, model)
        return res

    def basicInfo(self, model):
        '''Primed call to 'getInfo'. Returns a JSON :
        {'first_name_field': '......',
         'middle_name_field': '.....',
         'last_name_field': '......',
         'mobile_number': '......',
         'email' : '.......'
        }
        '''
        fields = ['first_name_field', 'middle_name_field', 'last_name_field', 'communication_mobtel1_field', 'communication_email1_field']
        return self.getInfo(model, fields)
        return res

class OO():

    apibase = ""

    baseurl  = "http://apiteststand.onlyonce.com"
    version  = "v2"

    seckey   = None
    apisec   = None
    apikey   = None

    username = None
    password = None

    bearer   = None

    network  = []
    cardsReceived = []

    lastCardSync = None

    random_names = {}

    def signin(self):


        if not self.username:
            raise Exception, "Cannot signin without your username"
        if not self.password:
            raise Exception, "Cannot signin without your password"

        self.apibase = self.baseurl + "/" + self.version
        payload = "{\"username\" : \"" + self.username + "\",\n \"password\" : \"" + self.password + "\"\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache"
        }

        response = requests.request("POST", self.apibase + "/signIn", data=payload, headers=headers)
        if response.status_code != 200:
            raise Exception, "Faulty Signin"
        self.bearer = response.headers['Authorization']
        return True


    def profiles(self,scope='MINE'):
        '''Return profiles
        scope = MINE (Default) All profiles owned by the authenitcated user
        scope = BOOKMARKS All bookmarked profiles
        scope = CONNECTIONS All profiles sharing data with, or receiving data from
        '''

        if not self.bearer:
            raise Exception, "No bearer token present, use signin first"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'Authorization': self.bearer
        }

        res = []
        response = requests.request("GET", self.apibase + "/profiles?scope=%s" % scope, headers=headers)
        for p in response.json()['content']:
            profile = {}
            profile['name'] = p['name']
            profile['id'] = p['id']
            profile['ooid'] = p['onlyonceId']
            profile['type'] = p['type']
            inc = p['incomingSharesCount']
            out = p['outgoingSharesCount']
            connections = inc + out
            if inc > out:
                profile['kind'] = 'CONSUMER'
            else:
                profile['kind'] = 'PROVIDER'
            res.append(profile)
        return res



    def connect(self):
        self.apibase  = self.baseurl + "/" +  self.version
        if not self.bearer:
            raise Exception, "No bearer token present, use register first"


    def cardsAge(self):
        '''Returns time since last cards-sync in seconds. Returns 9999 if no
        sync has been performed yet'''
        if lastCardSync == None:
            return 9999
        else:
            return (datetime.datetime.now() - lastCardSync).seconds

    def cards(self, profile, scope='ACCEPTED', maxAge=60):
        self.apibase  = self.baseurl + "/" +  self.version
        '''Returns all cards shared with me. Saves API calls by not refreshing
        within maxAge seconds. To get own cards, set scope to MINE
        '''
        #TODO: When calling with different scope, make sure to always refresh. Or keep two caches!


        if self.cardsAge > maxAge:
            headers = {
                'content-type': "application/json",
                'Authorization': self.bearer,
                'cache-control': "no-cache"
            }

            response = requests.request("GET", self.apibase + "/profiles/" + profile + "/cards?scope=" + scope , headers=headers)
            j = response.json()
            if j['content']:
                all_cards = len(j['content'])
                page = 0
                # This may return a paginated respsonse....
                while all_cards < response.json()['total']:
                    page += 1
                    response = requests.request("GET", self.apibase + "/profiles/" + profile + "/cards?scope=" + scope + "&page=" + str(page), headers=headers)

                    for to_add in response.json()['content']:
                        j['content'].append(to_add)
                    all_cards += len(response.json()['content'])
                self.cardsReceived = []
                for card in j['content']:
                    c = {}
#TODO make this a call to lookup the card (and cache it)
                    c['owner'] = card['ownerId']
                    c['name'] = card['name']
                    c['id'] = card['id']
                    self.cardsReceived.append(c)
                self.lastCardSync = datetime.datetime.now()

        return self.cardsReceived

    def connections(self):
        '''Returns a list of all unique users who have shared data with you.
        Returns empty list if no data shared with you, or you have not called 'cards' yet
        '''
        connections = []
        for card in self.cardsReceived:
            if card['owner'] not in connections:
                connections.append(card['owner'])
        return connections



    def card(self, cardid, seckey=None):
        '''Returns the full card JSON'''
        if not seckey:
            raise Exception, "You need to provide your secret key for us to decrypt your data"
        self.apibase  = self.baseurl + "/" +  self.version
        headers = {
            'content-type': "application/json",
            'authorization':  self.bearer,
            'Secret-Key': seckey,
            'cache-control': "no-cache"
            }

        response = requests.request("GET", self.apibase + "/cards/" + cardid, headers=headers)
        if response.status_code == 200:
            return response.json()

    def consolidated_view(self):
        '''Returns a list of all your network with all their cards mashed-up into one bit card
        '''

    def register(self):
        self.apibase  = self.baseurl + "/" +  self.version
        if not self.apikey:
            raise Exception, "Cannot connect without you API-key. Unable to register"
        if not self.apisec:
            raise Exception, "Cannot connect without you API-secret. Unable to register"

        payload = "{\"apiSecret\" : \"" + self.apisec + "\",\n \"apiKey\" : \"" + self.apikey + "\"\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache"
        }

        response = requests.request("POST", self.apibase + "/token", data=payload, headers=headers)
        self.bearer = response.headers['Authorization']
        return True





