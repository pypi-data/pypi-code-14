# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import os
from flask import json

from .test_settings import LDAP_SERVER, AMAZON_CONTAINER_NAME, \
    AMAZON_ACCESS_KEY_ID, AMAZON_SECRET_ACCESS_KEY, AMAZON_REGION, \
    AMAZON_SERVE_DIRECT_LINKS, AMAZON_S3_USE_HTTPS, AMAZON_SERVER, \
    AMAZON_PROXY_SERVER, AMAZON_URL_GENERATOR
from apps.io.tests import setup_providers, teardown_providers
from features.steps.steps import get_macro_path
from superdesk import tests
from superdesk.factory.app import get_app
from superdesk.tests import setup_auth_user
from superdesk.vocabularies.command import VocabulariesPopulateCommand


readonly_fields = ['display_name', 'password', 'phone', 'first_name', 'last_name']


def setup_before_all(context, config, app_factory):
    if AMAZON_CONTAINER_NAME:
        config['AMAZON_CONTAINER_NAME'] = AMAZON_CONTAINER_NAME
        config['AMAZON_ACCESS_KEY_ID'] = AMAZON_ACCESS_KEY_ID
        config['AMAZON_SECRET_ACCESS_KEY'] = AMAZON_SECRET_ACCESS_KEY
        config['AMAZON_REGION'] = AMAZON_REGION
        config['AMAZON_SERVE_DIRECT_LINKS'] = AMAZON_SERVE_DIRECT_LINKS
        config['AMAZON_S3_USE_HTTPS'] = AMAZON_S3_USE_HTTPS
        config['AMAZON_SERVER'] = AMAZON_SERVER
        config['AMAZON_PROXY_SERVER'] = AMAZON_PROXY_SERVER
        config['AMAZON_URL_GENERATOR'] = AMAZON_URL_GENERATOR

    # set the MAX_TRANSMIT_RETRY_ATTEMPT to zero so that transmit does not retry
    config['MAX_TRANSMIT_RETRY_ATTEMPT'] = 0
    tests.setup(context=context, config=config, app_factory=app_factory)
    os.environ['BEHAVE_TESTING'] = '1'


def setup_before_scenario(context, scenario, config, app_factory):
    if scenario.status != 'skipped' and 'notesting' in scenario.tags:
        config['SUPERDESK_TESTING'] = False

    tests.setup(context=context, config=config, app_factory=app_factory)
    context.headers = [
        ('Content-Type', 'application/json'),
        ('Origin', 'localhost')
    ]

    if 'dbauth' in scenario.tags and LDAP_SERVER:
        scenario.mark_skipped()

    if 'ldapauth' in scenario.tags and not LDAP_SERVER:
        scenario.mark_skipped()

    if 'amazons3' in scenario.tags and not context.app.config.get('AMAZON_CONTAINER_NAME', None):
        scenario.mark_skipped()

    if 'alchemy' in scenario.tags and not context.app.config.get('KEYWORDS_KEY_API'):
        scenario.mark_skipped()

    setup_search_provider(context.app)

    if scenario.status != 'skipped' and 'auth' in scenario.tags:
        setup_auth_user(context)

    if scenario.status != 'skipped' and 'provider' in scenario.tags:
        setup_providers(context)

    if scenario.status != 'skipped' and 'vocabulary' in scenario.tags:
        with context.app.app_context():
            cmd = VocabulariesPopulateCommand()
            filename = os.path.join(os.path.abspath(os.path.dirname("features/steps/fixtures/")), "vocabularies.json")
            cmd.run(filename)

    if scenario.status != 'skipped' and 'content_type' in scenario.tags:
        with context.app.app_context():
            cmd = VocabulariesPopulateCommand()
            filename = os.path.join(os.path.abspath(os.path.dirname("features/steps/fixtures/")), "content_types.json")
            cmd.run(filename)

    if scenario.status != 'skipped' and 'notification' in scenario.tags:
        tests.setup_notification(context)


def before_all(context):
    config = {}
    setup_before_all(context, config, app_factory=get_app)


def before_feature(context, feature):
    if 'tobefixed' in feature.tags:
        feature.mark_skipped()

    if 'dbauth' in feature.tags and LDAP_SERVER:
        feature.mark_skipped()

    if 'ldapauth' in feature.tags and not LDAP_SERVER:
        feature.mark_skipped()

    if 'amazons3' in feature.tags and not context.app.config.get('AMAZON_CONTAINER_NAME', None):
        feature.mark_skipped()


def before_scenario(context, scenario):
    config = {}
    setup_before_scenario(context, scenario, config, app_factory=get_app)


def after_scenario(context, scenario):
    if 'provider' in scenario.tags:
        teardown_providers(context)

    if 'notification' in scenario.tags:
        tests.teardown_notification(context)

    if 'clean' in scenario.tags:
        try:
            os.remove(get_macro_path('behave_macro.py'))
            os.remove(get_macro_path('validate_headline_macro.py'))
        except:
            pass


def before_step(context, step):
    if LDAP_SERVER and step.text:
        try:
            step_text_json = json.loads(step.text)
            step_text_json = {k: step_text_json[k] for k in step_text_json.keys() if k not in readonly_fields} \
                if isinstance(step_text_json, dict) else \
                [{k: json_obj[k] for k in json_obj.keys() if k not in readonly_fields} for json_obj in step_text_json]

            step.text = json.dumps(step_text_json)
        except:
            pass


def setup_search_provider(app):
    from apps.search_providers import register_search_provider, allowed_search_providers
    if 'testsearch' not in allowed_search_providers:
        register_search_provider('testsearch', 'testsearch')
