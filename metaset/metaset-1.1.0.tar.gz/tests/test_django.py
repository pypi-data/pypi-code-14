# -*- coding: utf-8 -*-
from .django_test_app import models as test_models

from django.test import runner
from django.test import TestCase
from django.test import utils
from nose.plugins.skip import SkipTest
from metaset import MetaSet


# Setup Django test environment
state = {}


def setUpModule():
    utils.setup_test_environment()
    state['runner'] = runner.DiscoverRunner(interactive=False)
    state['databases'] = state['runner'].setup_databases()


def tearDownModule():
    state['runner'].teardown_databases(state['databases'])
    utils.teardown_test_environment()


# the refresh_from_db method only came in with 1.8, use our own.
def refresh_from_db(obj):
    obj = obj.__class__.objects.get(id=obj.id)


class DjangoTest(TestCase):
    def test_save_load(self):
        obj = test_models.TestModel.objects.create(
            value={'a': set([1]), 'b': set([2, 3])})
        refresh_from_db(obj)
        assert obj.value == MetaSet({'a': {1}, 'b': {2, 3}})

    def test_query(self):
        try:
            from django.contrib.postgres.fields import JSONField  # noqa: F401
        except ImportError:
            raise SkipTest(
                "JSON queries are only available "
                "for native Django (>=1.9) JSONField")

        obj = test_models.TestModel.objects.create(
            value={'a': {1}, 'b': {2, 3}})
        res = test_models.TestModel.objects.filter(value__b__contains=[2])
        assert obj == res.first()
        res = test_models.TestModel.objects.filter(value__has_key='a')
        assert obj == res.first()

    def test_inception(self):
        obj = test_models.TestModel.objects.create(
            value={'a': {'b': {1}, 'c': {2, 3}}, 'd': {'e': {4}}}
            )
        refresh_from_db(obj)
        assert obj.value == MetaSet(
            a=MetaSet(b={1}, c={2, 3}),
            d=MetaSet(e={4}),
            )
