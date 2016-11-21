# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
from datetime import date
from .services import set_es_url

from elasticsearch import Elasticsearch

from celery import shared_task

def datetime_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError

@shared_task(serializer='json')
def task_http_log(es_log_data):
    body = json.dumps(es_log_data, default=datetime_handler)

    es = Elasticsearch(set_es_url())
    es.index(index='cd_http_log_{}'.format(date.today()),doc_type='log',body=body)
