# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from datetime import datetime
import os

from timelineio.clients import TimelineIOClient
from timelineio.utils import env_to_bool


def create_event(base_api_url, auth_token, message, timestamp, object_id, object_type, human_identifier):
    client = TimelineIOClient(base_api_url=base_api_url, auth_token=auth_token)
    return client.Event.create(
        message=message,
        timestamp=timestamp,
        object_id=object_id,
        object_type=object_type,
        human_identifier=human_identifier
    )

if env_to_bool('TIMELINEIO_ASYNC'):
    from celery import shared_task
    create_event = shared_task(create_event)
    create_event = create_event.delay


class TimelineIOModelMixin(object):
    TIMELINEIO_IDENTIFIER_FIELD = 'id'
    TIMELINEIO_HUMAN_IDENTIFIER_FIELD = None

    def _fully_qualified_object_path(self):
        return '{}.{}'.format(self.__class__.__module__, self.__class__.__name__)

    def timelineio(self, message, timestamp=None):
        if not env_to_bool('TIMELINEIO_ENABLED', default=True):
            return

        if not timestamp:
            timestamp = datetime.utcnow()

        try:
            base_api_url = os.environ['TIMELINEIO_URL']
            auth_token = os.environ['TIMELINEIO_ACCESS_KEY']
        except KeyError:
            raise RuntimeError(
                'In order to use TimelineIO you *must* set both TIMELINEIO_URL and TIMELINEIO_ACCESS_KEY env vars.'
            )

        object_id = str(getattr(self, self.TIMELINEIO_IDENTIFIER_FIELD))
        object_type = self._fully_qualified_object_path()
        timestamp = timestamp.isoformat()

        if self.TIMELINEIO_HUMAN_IDENTIFIER_FIELD:
            human_identifier = getattr(self, self.TIMELINEIO_HUMAN_IDENTIFIER_FIELD)
        else:
            human_identifier = '{}'.format(self)

        return create_event(base_api_url, auth_token, message, timestamp, object_id, object_type, human_identifier)
