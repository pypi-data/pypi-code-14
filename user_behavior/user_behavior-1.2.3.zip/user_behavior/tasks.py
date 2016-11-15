# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
from datetime import date
from django.forms import model_to_dict
from .services import set_es_url

from elasticsearch import Elasticsearch

from celery import shared_task


@shared_task(serializer='json')
def task_user_behavior(api_info):

    es = Elasticsearch(set_es_url())
    body = json.dumps(model_to_dict(api_info))

    try:
        es.index(index='cd_event_log_{}'.format(date.today()),
                doc_type='log',
                body=json.dumps(body))
    except Exception:
        pass
