# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json
from redis import StrictRedis, ConnectionPool

from jobminer.queue.base import BaseJobQueue


class RedisMultiplex(object):
    def __init__(self, host='127.0.0.1', port=6379, db=0, password=None):
        self.pool = ConnectionPool(
            host=host,
            port=port,
            db=db,
            password=password,
        )
        self.redis = StrictRedis(connection_pool=self.pool)

    def _calculate_job_key(self, phase_identity):
        key = 'phase.{0}.jobs'.format(phase_identity)
        return key

    def _calculate_result_key(self, phase_identity):
        key = 'phase.{0}.results'.format(phase_identity)
        return key

    def serialize(self, data):
        return json.dumps(data)


class RedisJobQueue(BaseJobQueue):
    def initialize(self, host='127.0.0.1', port=6379, db=0, password=None):
        self.connection = RedisMultiplex(host, port, db, password)

    def consume_for_phase(self, phase_identity):
        key = self._calculate_job_key(phase_identity)
        return self.redis.lpop(key)

    def schedule_for_phase(self, phase_identity, data):
        key = self._calculate_job_key(phase_identity)
        serialized = self.serialize(data)
        return self.redis.rpush(key, serialized)

    def count_remaining_for_phase(self, phase_identity):
        key = self._calculate_job_key(phase_identity)
        return self.redis.llen(key)

    def store_finished_job(self, phase_identity, data):
        key = self._calculate_result_key(phase_identity)
        serialized = self.serialize(data)
        return self.redis.rpush(key, serialized)

    def get_finished_jobs(self, phase_identity):
        key = self._calculate_result_key(phase_identity)
        return self.redis.lrange(key, 0, -1)
