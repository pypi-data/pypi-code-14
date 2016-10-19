# oopyconnector : python framework for connecting to the Only Once API
#
#
# Author(s)     :   - Henri Kuiper (henri.kuiper@onlyonce.com)

#
#
# Version       : 2.0beta

import requests
import datetime
import logging

import names

logging.basicConfig(filename="oopyconnector.log", level=logging.DEBUG,format='%(asctime)s %(message)s')

def debug(message):
    logging.debug(message)

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
        else:
            return None

    def getInfo(self, card, fields):
        '''Retrieves all fields from a card. Fields should be speicifed as a list of 'strings'.
        '''
        res = {}
        for field in fields:
            res[field] = self.findField(field, card['model'][0])
        return res

    def basicInfo(self, card):
        '''Primed call to 'getInfo'. Returns a JSON :
        {'first_name_field': '......',
         'middle_name_field': '.....',
         'last_name_field': '......',
         'mobile_number': '......',
         'email' : '.......'
        }
        '''
        fields = ['first_name_field', 'middle_name_field', 'last_name_field', 'communication_mobtel1_field', 'communication_email1_field']
        return self.getInfo(card, fields)

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
    profileAccessEnabled = False

    random_names = {}

    def signin(self):

        debug("Doing signin for user <%s>" % self.username)


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

    def signout(self):
        '''Returns public card for a profile'''
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'Authorization': self.bearer
        }
        response = requests.request("GET", self.apibase + "/signOut", headers=headers)
        print "SIGNOUT: %s" % response


    def datastore(self, profile=None):
        '''return it, if there is a profile'''
        self.getAccess(profile)
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'Authorization': self.bearer
        }
        response = requests.request("GET", self.apibase + "/profiles/%s/dataStore" % profile, headers=headers)
        return response.json()

    def profile(self, profileid):
        '''Returns public card for a profile'''
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'Authorization': self.bearer
        }
        response = requests.request("GET", self.apibase + "/profiles/%s" % profileid, headers=headers)
        return response.json()

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
            profile['inc'] = p['incomingSharesCount']
            profile['out'] = p['outgoingSharesCount']
            if profile['inc'] > profile['out']:
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

    def getAccess(self, profile=None):
        '''Some endpoints require acccess. Access is granted if this endpoint is hit with a correct secret key for the
        accompanying profile.
        '''
        if not self.seckey:
            raise Exception, "You need to provide your secret key for us to enable access to your encrypted data"
        if not profile:
            raise Exception, "You need to specify a profile"
        headers = {
            'content-type': "application/json",
            'Authorization': self.bearer,
            'Secret-Key': self.seckey,
            'cache-control': "no-cache"
        }

        response = requests.request("POST", self.apibase + "/profiles/" + profile + "/access", headers=headers)

        if response.status_code == 200:
            self.profileAccessEnabled = True

        return True


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



    def card(self, profileid, cardid):
        '''Returns the full card JSON'''

        if not self.profileAccessEnabled:
            self.getAccess(profileid)
        self.apibase  = self.baseurl + "/" +  self.version
        headers = {
            'content-type': "application/json",
            'authorization':  self.bearer,
            'cache-control': "no-cache"
            }

        response = requests.request("GET", self.apibase + "/profiles/" + profileid + "/cards/" + cardid, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception, "Cannot return card, decryption not possible. Secret-Key not sent via /access endpoint"

    def consolidated_view(self):
        '''Returns a list of all your network with all their cards mashed-up into one bit card
        '''






