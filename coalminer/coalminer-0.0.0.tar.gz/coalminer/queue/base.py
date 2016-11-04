# -*- coding: utf-8 -*-


class BaseJobQueue(object):
    def __init__(self, *args, **kw):
        self.initialize(*args, **kw)

    def initialize(self):
        pass

    def consume_for_phase(self, phase_identity):
        pass

    def schedule_for_phase(self, phase_identity, data):
        pass

    def count_remaining_for_phase(self, phase_identity):
        return 0

    def store_finished_job(self, phase_identity, data):
        return False

    def get_finished_jobs(self, phase_identity, data):
        return []
