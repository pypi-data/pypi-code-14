import webapp2
from google.appengine.api import users
import json
import logging
import os
import sys
import httplib2
import pickle

from googleapiclient import discovery
from oauth2client import client
from oauth2client.contrib import appengine
from google.appengine.api import memcache

from google.appengine.api import app_identity
from google.appengine.ext import ndb


class RestEntity(webapp2.RequestHandler):

    def __init__(self, request, response):
        self.initialize(request, response)
        self.response.content_type = 'application/json'
        self.is_admin = users.is_current_user_admin()
        if users.get_current_user():
            self.user_id = users.get_current_user().user_id()
        else:
            self.user_id = self.get_oauth2_user_id()
        if not self.user_id:
            self.abort(401)

    def get(self, id):
        results = []
        if not id:
            xs = self.entity.get_by_user_id(self.user_id)
            results = [x.to_dict() for x in xs] if xs is not None else []
        else:
            x = self.entity.get_by_id(int(id))
            if not self.is_admin:
                if x.user_id != self.user_id:
                    self.abort(401)
            results = x.to_dict()

        self.response.write(json.dumps(results))

    def post(self, id):
        payload = json.loads(self.request.body)
        entities = []
        if type(payload) is list:
            entities = [self.create_entity(x) for x in payload]
        else:
            entities = [self.create_entity(payload)]

        ndb.put_multi(entities)

        result = [x.to_dict() for x in entities]

        self.response.write(json.dumps(result))

    def create_entity(self, payload):
        u = str(payload.get('user_id').encode(
            'utf-8')) if 'user_id' in payload else None

        if not self.is_admin:
            if (u is not None) and (u != self.user_id):
                self.abort(401)

            payload['user_id'] = self.user_id
        else:
            if u is None or u == "":
                payload['user_id'] = self.user_id

        created = self.entity(**payload)
        return created

    def delete(self, id):
        m = self.entity.get_by_id(int(id))
        if not m:
            self.abort(404)
        if m.user_id != self.user_id:
            self.abort(401)
        self.entity.key.delete(id)

    def get_oauth2_user_id(self):
        token = self.request.headers.get('Authorization')
        if token:
            auth_type, credentials = token.split(' ')
            credentials = client.AccessTokenCredentials(
                credentials,
                None)
            http_auth = credentials.authorize(httplib2.Http())
            service = discovery.build("plus", "v1", http=http_auth)
            user = service.people().get(userId='me').execute()
            print 'user:', user
            return user.get('id')
