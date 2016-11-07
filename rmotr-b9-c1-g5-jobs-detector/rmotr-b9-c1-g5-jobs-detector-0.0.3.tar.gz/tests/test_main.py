# -*- coding: utf-8 -*-
import re
import os
import unittest

import responses
from click.testing import CliRunner

from jobs_detector import settings
from jobs_detector.main import jobs_detector


class HackerNewsTestCase(unittest.TestCase):

    def setUp(self):
        self.post_id = '11814828'
        fixture_path = os.path.join(settings.BASE_DIR, 'tests',
                                    'fixtures', '{}.html'.format(self.post_id))
        with open(fixture_path) as f:
            content = f.read()
        responses.add(responses.GET,
                      re.compile(re.escape(settings.BASE_URL.format(self.post_id))),
                      body=content, status=200,
                      content_type='text/html')

    @responses.activate
    def test_hacker_news_default_keywords(self):
        runner = CliRunner()
        result = runner.invoke(
            jobs_detector,
            ['hacker_news', '-i', self.post_id]
        )
        expected = [
            'Total job posts: 691',

            'Keywords:',
            'Remote: 153 (22%)',
            'Postgres: 81 (11%)',
            'Python: 143 (20%)',
            'Javascript: 117 (16%)',
            'React: 131 (18%)',
            'Pandas: 5 (0%)',
        ]
        for msg in expected:
            self.assertTrue(msg in result.output)

    @responses.activate
    def test_hacker_news_custom_keywords(self):
        runner = CliRunner()
        result = runner.invoke(
            jobs_detector,
            ['hacker_news',
             '-i', self.post_id,
             '-k', 'python,django']
        )
        expected = [
            'Total job posts: 691',

            'Keywords:',
            'Python: 143 (20%)',
            'Django: 36 (5%)',
        ]
        for msg in expected:
            self.assertTrue(msg in result.output)

    @responses.activate
    def test_hacker_news_combinations(self):
        runner = CliRunner()
        result = runner.invoke(
            jobs_detector,
            ['hacker_news',
             '-i', self.post_id,
             '-c', 'python-remote,python-django,django-remote']
        )
        expected = [
            'Total job posts: 691',

            'Keywords:',
            'Remote: 153 (22%)',
            'Postgres: 81 (11%)',
            'Python: 143 (20%)',
            'Javascript: 117 (16%)',
            'React: 131 (18%)',
            'Pandas: 5 (0%)',

            'Combinations:',
            'Python-Remote: 25 (3%)',
            'Django-Remote: 6 (0%)',
            'Python-Django: 35 (5%)',
        ]
        for msg in expected:
            self.assertTrue(msg in result.output)

    @responses.activate
    def test_hacker_news_keywords_and_combinations(self):
        runner = CliRunner()
        result = runner.invoke(
            jobs_detector,
            ['hacker_news',
             '-i', self.post_id,
             '-k', 'python,django',
             '-c', 'python-remote,python-django,django-remote']
        )
        expected = [
            'Total job posts: 691',

            'Keywords:',
            'Python: 143 (20%)',
            'Django: 36 (5%)',

            'Combinations:',
            'Python-Remote: 25 (3%)',
            'Django-Remote: 6 (0%)',
            'Python-Django: 35 (5%)',
        ]
        for msg in expected:
            self.assertTrue(msg in result.output)