#! /usr/python/env python
# -*- coding:utf-8 -*-

import os
import sys
import logging
import logging.config
import getpass
import platform
from datetime import datetime
import time
import random
from ConfigParser import ConfigParser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from errors import (ADCFileUnFoundError,
                    ADCMissingRequiredOptionError,
                    ADCTypeError,
                    ADCInvalidSettingError,
                    ADCSettingValueTypeError,)

from handler import FunctionHandler
# HOME_DIR=os.path.abspath("%s/../" %(os.path.split(os.path.realpath(__file__))[0]))
# print("HOME_DIR=%s" %(HOME_DIR))
# sys.path.append(HOME_DIR)
from entities import (ADCUserLogs,
                           ADCDataset,
                           ADCDatasetRelationship,)

from settings import APISettings

from builder import (ExecutorBuilder,
                     SQLSessionBuilder,)

_logger = logging.getLogger(__name__)


class ADCloudDriver(object):

    def __init__(self, conf_path, api_config):
        # try:
        if not os.path.exists(conf_path):
            raise ADCFileUnFoundError(
                "the file %s not exists." % (conf_path))

        config = ConfigParser()
        config.read(conf_path)

        self._db_connect_url = config.get(
            "driver_config", "db_connect_url")

        if self._db_connect_url is None:
            raise ADCMissingRequiredOptionError(
                "This 'db_connect_url' option must be set in the config of %s." % (conf_path))

        self.api_config = api_config

        if not isinstance(self.api_config, dict):
            raise ADCTypeError(
                "The parameter of 'api_config' should be a dict type.")

        _logger.info("db_connect_url:%s" % (self._db_connect_url))

        # self._db_engine = create_engine(
        #     self._db_connect_url, encoding="utf-8", echo=False)
        # self._session = None
        # self._init_session()
        _logger.info(self.api_config)

        self._session_builder=SQLSessionBuilder(**{'db_connect_url':self._db_connect_url})

        self._api_settings = APISettings(self._session_builder,self.api_config)

        self._username = getpass.getuser()
        self._hostname = platform.node()

        _logger.addHandler(FunctionHandler(
            level=logging.INFO, handle_func=self._handle_func))

        self._job_id = "job_%s_%s" % (
            long(time.time()), random.randint(100000, 900000))
        _logger.info("start")

        self._executor=ExecutorBuilder.build(self._api_settings)

        _logger.info("api config:%s" %(self.api_config))
        _logger.info("run sql:%s" %(self._executor.sql))


    def execute(self):
        return self._executor.execute()

    def executeAndSave(self, local_path):
        self._executor.executeAndSave(local_path)

    def _handle_func(self, record):
        session=self._session_builder.getSession()

        session.add(ADCUserLogs(level=record.levelname, job_id=self._job_id, log_type='',
                                      user=self._username, host=self._hostname, message=record.getMessage()))
        session.commit()


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S')
    #db_connect_url = 'mysql://autoax:autoax@10.168.100.50:3306/adcloud?charset=utf8'
    #db_connect_url = 'mysql://autoax:autoax@10.168.100.50:3306/adcloud?charset=utf8'
    #engine = create_engine(db_connect_url, encoding="utf-8", echo=True)

    # api_settings = {
    #     "dataset": 23,
    #     "fields": ['sdate', 'hour', 'creative_id','group_name', 'adpos_id','adpos_name'],
    #     "filter": "sdate>=20160824 and sdate<=20160826 and creative_id in('373789','373325','373601')",
    #     "aggregate": [('req_num','sum'), ('vis_display_num','sum'), ('click_num','sum')],
    #     "groups": ['sdate', 'hour', 'creative_id','group_name', 'adpos_id','adpos_name'],
    #     "sort": [('sdate', 'desc'), ('hour', 'asc')],
    #     "limits": 100,
    # }

    # api_settings = {
    #     "dataset": 60,
    #     "fields": ['adpos_id', 'adpos_name','website','page', 'channelfirst', 'channelsecond'],
    #     "filter": "adpos_id in('1006','1007','1008')",
    #     "sort": [('adpos_id', 'desc')],
    #     "limits": 100,
    # }

    # api_settings = {
    #     "dataset": 23,
    #     "fields": ['sdate', 'hour', 'creative_id','group_name', 'adpos_id','adpos_name'],
    #     "filter": "sdate>=20160824 and sdate<=20160826 and creative_id in('373789','373325','373601')",
    #     "sort": [('sdate', 'desc'), ('hour', 'asc')],
    #     "limits": 100,
    # }

    conf = {
        "dataset": 23,
        "fields": ['sdate', 'hour', 'creative_id','adpos_id','req_num'],
        "filter": "sdate>=20160824 and sdate<=20160826 and creative_id in('373789','373325','373601')",
        "sort": [('sdate', 'desc'), ('hour', 'asc')],
        "limits": 100,
   	} 

#    conf = {
#        "dataset": 111,
#        "fields": ['sdate', 'hour', 'creative_id','group_name', 'adpos_id','adpos_name'],
#        "filter": "sdate>=20160824 and sdate<=20160826 and creative_id in('373789','373325','373601')",
#        "aggregate": [('req_num','sum'), ('vis_display_num','sum'), ('click_num','sum')],
#        "groups": ['sdate', 'hour', 'creative_id','group_name', 'adpos_id','adpos_name'],
#        "sort": [('sdate', 'desc'), ('hour', 'asc')],
#        "limits": 100,
#    }

    # conf = {
    #     "dataset": 111,
    #     "fields": ['sdate', 'hour', 'creative_id','group_name', 'adpos_id','adpos_name'],
    #     "filter": "sdate>=20160824 and sdate<=20160826 and creative_id in('373789','373325','373601')",
    #     "aggregate": [('req_num','sum'), ('vis_display_num','sum'), ('click_num','sum')],
    #     "groups": ['sdate', 'hour', 'creative_id','group_name', 'adpos_id','adpos_name'],
    #     "sort": [('sdate', 'desc'), ('hour', 'asc')],
    #     "limits": 100,
    # }

    driver = ADCloudDriver("../conf/driver.cfg", conf)
    rows=driver.execute()
    for row in rows:
        print(",".join(row))

    driver.executeAndSave("./save.data")


