from __future__ import absolute_import, division, print_function, unicode_literals

import datetime
import requests

import tiros.util as util
from tiros.auth import AuthSession
from tiros.util import pretty, eprint, vprint

# Use new-style classes in Python 2
__metaclass__ = type


API_VERSION = 1
DEV_HOST = 'dev.tiros.amazonaws.com'
PROD_HOST = 'prod.tiros.amazonaws.com'


def get_route(command):
    return ''.join(['/v', str(API_VERSION), '/', command])


def get_endpoint(ssl, host, route):
    if host in [DEV_HOST, PROD_HOST] and not ssl:
        eprint("You must use SSL with the dev and prod hosts")
    proto = 'https' if ssl else 'http'
    return ''.join([proto, '://', host, route])


def get_headers(amz_date, auth_header, signing_session):
    headers = {
        'Authorization': auth_header,
        'Content-Type': util.CONTENT_TYPE,
        'X-Amz-Date': amz_date
    }
    token = signing_session.token()
    if token:
        headers['X-Amz-Security-Token'] = token
    return headers


def snapshot(signing_session,
             snapshot_sessions=None,
             snapshots=None,
             raw_snapshots=None,
             ssl=True,
             host=PROD_HOST):
    """
    Create a JSON snapshot containing the combined networks.

    :param signing_session:
    :param snapshot_sessions:
    :param snapshots:
    :param raw_snapshots:
    :param ssl:
    :param host:
    :return:
    """
    # noinspection PyUnresolvedReferences
    now = datetime.datetime.utcnow()
    amz_date = now.strftime('%Y%m%dT%H%M%SZ')
    date_stamp = now.strftime('%Y%m%d')
    route = get_route('snapshot')
    endpoint = get_endpoint(ssl, host, route)
    auth_sessions = [AuthSession(p) for p in (snapshot_sessions or [])]
    obj_body = (
        [{'credentials': s.snapshot_key(amz_date, date_stamp, host)}
         for s in auth_sessions] +
        [{'snapshot': s} for s in (snapshots or [])] +
        [{'raw_snapshot': s} for s in (raw_snapshots or [])]
    )
    body = util.canonical(obj_body)
    auth_session = AuthSession(signing_session)
    auth_header = auth_session.auth_header(
        amz_date, body, date_stamp, host, util.METHOD, route)
    headers = get_headers(amz_date, auth_header, auth_session)
    vprint('Headers: ' + pretty(headers))
    return requests.request(util.METHOD, endpoint, headers=headers, data=body)


def query(signing_session,
          queries,
          snapshot_sessions=None,
          snapshots=None,
          raw_snapshots=None,
          backend=None,
          transforms=None,
          user_relations=None,
          ssl=True,
          host=PROD_HOST):
    """
    :param signing_session:
    :param queries:
    :param snapshot_sessions:
    :param snapshots:
    :param raw_snapshots:
    :param backend:
    :param transforms:
    :param user_relations:
    :param ssl:
    :param host:
    :return:
    """
    # noinspection PyUnresolvedReferences
    now = datetime.datetime.utcnow()
    amz_date = now.strftime('%Y%m%dT%H%M%SZ')
    date_stamp = now.strftime('%Y%m%d')
    route = get_route('query')
    endpoint = get_endpoint(ssl, host, route)
    auth_sessions = [AuthSession(p) for p in (snapshot_sessions or [])]
    dbs = (
        [{'credentials': s.snapshot_key(amz_date, date_stamp, host)}
         for s in auth_sessions] +
        [{'snapshot': s} for s in (snapshots or [])] +
        [{'raw_snapshot': s} for s in (raw_snapshots or [])]
    )
    obj_body = {'queries':  queries, 'dbs': dbs}
    if backend:
        obj_body['backend'] = backend
    if transforms:
        obj_body['transforms'] = transforms
    if user_relations:
        obj_body['userRelations'] = user_relations
    vprint('Body: ' + pretty(obj_body))
    body = util.canonical(obj_body)
    auth_session = AuthSession(signing_session)
    auth_header = auth_session.auth_header(
        amz_date, body, date_stamp, host, util.METHOD, route)
    headers = get_headers(amz_date, auth_header, auth_session)
    vprint('Headers: ' + pretty(headers))
    return requests.request(util.METHOD, endpoint, headers=headers, data=body)
