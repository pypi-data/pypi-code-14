# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
from django.forms import model_to_dict
from datetime import date
from elasticsearch import Elasticsearch

from django.contrib.auth.models import User

from .serializers import ApiInfoSerializer
from .services import get_request_data, set_response_data


class UserBehaviorExtractMiddleWare(object):

    def process_request(self, request):
        request_data = get_request_data(request)

        serializer = ApiInfoSerializer(data=request_data, partial=True)

        if serializer.is_valid():
            user = User.objects.get(id=request.user.id)
            api_info = serializer.save(user=user)
            self._api_info = api_info

    def process_response(self, request, response):
        api_info = set_response_data(self._api_info, response)

        es = Elasticsearch('10.18.5.127:9200')
        es.index(index='cd_event_log_{}'.format(date.today()), doc_type='log', body=json.dumps(model_to_dict(api_info)))
        return response