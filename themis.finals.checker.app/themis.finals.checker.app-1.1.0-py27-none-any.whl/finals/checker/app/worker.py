# -*- coding: utf-8 -*-
from datetime import datetime
import dateutil.parser
from dateutil.tz import tzlocal
from base64 import urlsafe_b64encode, urlsafe_b64decode
from sys import exc_info
import requests
from themis.finals.api.auth import issue_checker_token
import os
from themis.finals.checker.result import Result
from imp import load_source
import logging
import raven


class Metadata(object):
    def __init__(self, options):
        self._timestamp = options.get('timestamp', None)
        self._round = options.get('round', None)
        self._team_name = options.get('team_name', u'')
        self._service_name = options.get('service_name', u'')

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def round(self):
        return self._round

    @property
    def team_name(self):
        return self._team_name

    @property
    def service_name(self):
        return self._service_name


logger = logging.Logger(__name__)

checker_module_name = os.getenv(
    'THEMIS_FINALS_CHECKER_MODULE',
    os.path.join(os.getcwd(), 'checker.py')
)
checker_module = load_source('', checker_module_name)

raven_enabled = os.getenv('SENTRY_DSN', None) is not None
raven_client = None
if raven_enabled:
    raven_client = raven.Client(dsn=os.getenv('SENTRY_DSN'))


def internal_push(endpoint, flag, adjunct, metadata):
    result, updated_adjunct = Result.INTERNAL_ERROR, adjunct
    try:
        raw_result = checker_module.push(endpoint, flag, adjunct, metadata)
        if isinstance(raw_result, tuple) and len(raw_result) == 2:
            result = raw_result[0]
            updated_adjunct = raw_result[1]
        else:
            result = raw_result
    except Exception:
        if raven_enabled:
            raven_client.captureException()
        logger.exception('An exception occurred', exc_info=exc_info())
    return result, updated_adjunct


def internal_pull(endpoint, flag, adjunct, metadata):
    result = Result.INTERNAL_ERROR
    try:
        result = checker_module.pull(endpoint, flag, adjunct, metadata)
    except Exception:
        if raven_enabled:
            raven_client.captureException()
        logger.exception('An exception occurred', exc_info=exc_info())
    return result


def queue_push(job_data):
    params = job_data['params']
    metadata = Metadata(job_data['metadata'])
    timestamp_created = dateutil.parser.parse(metadata.timestamp)
    timestamp_delivered = datetime.now(tzlocal())

    status, updated_adjunct = internal_push(
        params['endpoint'],
        params['flag'],
        urlsafe_b64decode(params['adjunct'].encode('utf-8')),
        metadata)

    timestamp_processed = datetime.now(tzlocal())

    job_result = dict(status=status.value,
                      flag=params['flag'],
                      adjunct=urlsafe_b64encode(updated_adjunct))

    delivery_time = (timestamp_delivered - timestamp_created).total_seconds()
    processing_time = (
        timestamp_processed - timestamp_delivered
    ).total_seconds()

    log_message = (u'PUSH flag `{0}` /{1:d} to `{2}`@`{3}` ({4}) - status {5},'
                   u' adjunct `{6}` [delivery {7:.2f}s, processing '
                   u'{8:.2f}s]').format(
        params['flag'],
        metadata.round,
        metadata.service_name,
        metadata.team_name,
        params['endpoint'],
        status.name,
        job_result['adjunct'],
        delivery_time,
        processing_time
    )

    if raven_enabled:
        short_log_message = u'PUSH `{0}...` /{1:d} to `{2}` - status {3}'.format(
            params['flag'][0:8],
            metadata.round,
            metadata.team_name,
            status.name
        )

        raven_client.captureMessage(
            short_log_message,
            level=logging.INFO,
            tags={
                'tf_operation': 'push',
                'tf_status': status.name,
                'tf_team': metadata.team_name,
                'tf_service': metadata.service_name,
                'tf_round': metadata.round
            },
            extra={
                'endpoint': params['endpoint'],
                'flag': params['flag'],
                'adjunct': job_result['adjunct'],
                'delivery_time': delivery_time,
                'processing_time': processing_time
            }
        )

    logger.info(log_message)

    uri = job_data['report_url']
    headers = {}
    headers[os.getenv('THEMIS_FINALS_AUTH_TOKEN_HEADER')] = \
        issue_checker_token()
    r = requests.post(uri, headers=headers, json=job_result)
    logger.info(r.status_code)


def queue_pull(job_data):
    params = job_data['params']
    metadata = Metadata(job_data['metadata'])
    timestamp_created = dateutil.parser.parse(metadata.timestamp)
    timestamp_delivered = datetime.now(tzlocal())

    status = internal_pull(
        params['endpoint'],
        params['flag'],
        urlsafe_b64decode(params['adjunct'].encode('utf-8')),
        metadata)

    timestamp_processed = datetime.now(tzlocal())

    job_result = dict(request_id=params['request_id'],
                      status=status.value)

    delivery_time = (timestamp_delivered - timestamp_created).total_seconds()
    processing_time = (
        timestamp_processed - timestamp_delivered
    ).total_seconds()

    log_message = (u'PULL flag `{0}` /{1:d} from `{2}`@`{3}` ({4}) with '
                   u'adjunct `{5}` - status {6} [delivery {7:.2f}s, '
                   u'processing {8:.2f}s]').format(
        params['flag'],
        metadata.round,
        metadata.service_name,
        metadata.team_name,
        params['endpoint'],
        params['adjunct'],
        status.name,
        delivery_time,
        processing_time
    )

    if raven_enabled:
        short_log_message = u'PULL `{0}...` /{1:d} from `{2}` - status {3}'.format(
            params['flag'][0:8],
            metadata.round,
            metadata.team_name,
            status.name
        )

        raven_client.captureMessage(
            short_log_message,
            level=logging.INFO,
            tags={
                'tf_operation': 'pull',
                'tf_status': status.name,
                'tf_team': metadata.team_name,
                'tf_service': metadata.service_name,
                'tf_round': metadata.round
            },
            extra={
                'endpoint': params['endpoint'],
                'flag': params['flag'],
                'adjunct': params['adjunct'],
                'delivery_time': delivery_time,
                'processing_time': processing_time
            }
        )

    logger.info(log_message)

    uri = job_data['report_url']
    headers = {}
    headers[os.getenv('THEMIS_FINALS_AUTH_TOKEN_HEADER')] = \
        issue_checker_token()
    r = requests.post(uri, headers=headers, json=job_result)
    logger.info(r.status_code)
