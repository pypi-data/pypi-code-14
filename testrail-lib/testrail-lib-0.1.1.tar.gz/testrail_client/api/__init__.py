#!/usr/bin/env python                                                                                                                                                
# -*- coding: utf-8 -*-

from .case import Case
from .configurations import Config
from .milestone import MileStone
from .plan import Plan
from .project import Project
from .result import Result
from .run import Run
from .section import Section
from .suite import Suite
from .test import Test
from .user import User


class TestRailAPI(object):
    __version__ = 'v2'

    def __init__(self, url, user_name, password):
        self.url = url
        self.user_name = user_name
        self.password = password
        
    def __repr__(self):
        return '<TestRail API>'

    @property
    def user(self):
        return User(self.url, self.user_name, self.password)

    @property
    def case(self):
        return Case(self.url, self.user_name, self.password)

    @property
    def config(self):
        return Config(self.url, self.user_name, self.password)

    @property
    def milestone(self):
        return MileStone(self.url, self.user_name, self.password)

    @property
    def plan(self):
        return Plan(self.url, self.user_name, self.password)

    @property
    def project(self):
        return Project(self.url, self.user_name, self.password)

    @property
    def result(self):
        return Result(self.url, self.user_name, self.password)

    @property
    def run(self):
        return Run(self.url, self.user_name, self.password)

    @property
    def section(self):
        return Section(self.url, self.user_name, self.password)

    @property
    def suite(self):
        return Suite(self.url, self.user_name, self.password)

    @property
    def test(self):
        return Test(self.url, self.user_name, self.password)
