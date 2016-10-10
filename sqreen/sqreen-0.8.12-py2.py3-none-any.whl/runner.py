# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Main runner module
"""

import logging
from time import time
from datetime import datetime

from .deliverer import get_deliverer

try:
    # Python2
    from queue import Empty, Queue, Full
except ImportError:
    from Queue import Empty, Queue, Full

MAX_QUEUE_LENGTH = 100
MAX_OBS_QUEUE_LENGTH = 1000

LOGGER = logging.getLogger(__name__)


class RunnerStop(object):
    """ Placeholder event for asking the runner to stop
    """


class MetricsEvent(object):
    """ Placeholder for asking observations aggregation to run
    """


class CappedQueue(object):
    """ Capped queue with opiniatied methods
    """

    def __init__(self, maxsize=None):
        if maxsize is None:
            maxsize = MAX_QUEUE_LENGTH

        self.maxsize = maxsize
        self.queue = Queue(self.maxsize)

    def get(self, timeout):
        """ Wait for up to timeout for an item to return and block while
        waiting
        """
        return self.queue.get(block=True, timeout=timeout)

    def get_nowait(self):
        """ Get without waiting, raise queue.Empty if nothing is present
        """
        return self.queue.get_nowait()

    def put(self, item):
        """ Tries to put an item to the queue, if the queue is empty, pop an
        item and try again
        """
        pushed = False
        while pushed is False:
            try:
                self.queue.put_nowait(item)
                pushed = True
            except Full:
                try:
                    self.queue.get_nowait()
                    self.queue.task_done()
                except Empty:
                    pass

    def clear(self):
        """ Clear all items in the queue
        """
        with self.queue.mutex:
            self.queue.queue.clear()

    def half_full(self):
        """ Return True if the current queue size if at least half the maxsize
        """
        return self.queue.qsize() > (self.maxsize / 2.)


class RunnerSettings(object):
    """ Various values that need to be shared across threads
    """

    def __init__(self):
        self.paths_whitelist = []

    def paths_whitelist_match(self, request_path):
        """ Check if the request_path starts with one of the whitelisted
        paths.
        """
        for path in self.paths_whitelist:
            if request_path.startswith(path):
                return path
        return None


class Runner(object):
    """ Main runner class

    Its job is to be the orchestrator and receiver for application communication
    It interacts with the backend through session, call heartbeat himself,
    execute commands and forward events
    """

    # At start, heartbeat is every 15 seconds
    HEARTBEAT_INITIAL_DELAY = 15
    # During one hour
    HEARTBEAT_WARMUP = 60 * 60
    # Then delay raises to 5 minutes
    HEARTBEAT_MAX_DELAY = 5 * 60

    def __init__(self, queue, observation_queue, session, deliverer,
                 remote_command, instrumentation, metrics_store,
                 settings, initial_features=None):
        self.logger = logging.getLogger('{}.{}'.format(self.__module__, self.__class__.__name__))
        self.queue = queue
        self.observation_queue = observation_queue
        self.deliverer = deliverer
        self.remote_command = remote_command
        self.instrumentation = instrumentation
        self.metrics_store = metrics_store
        self.settings = settings
        self.stop = False

        # Save the time runner started for checking warmup period termination
        self.started = time()

        if initial_features is None:
            initial_features = {}

        # The first time we shouldn't wait too long before sending heartbeat
        self.heartbeat_delay = self.HEARTBEAT_INITIAL_DELAY
        self.publish_metrics_delay = initial_features.get('publish_metrics_delay',
                                                          self.HEARTBEAT_MAX_DELAY)

        # Not used for the moment
        self.performance_metrics_period = initial_features.get('performance_metrics_period', 0)

        self.last_heartbeat_request = 0
        self.last_post_metrics_request = time()

        self.session = session

        self.logger.debug("Initial features %s", self.features_get())

    def run(self):
        """ Infinite loop
        """
        self.logger.debug("Starting runner")
        while self.stop is False:
            self.run_once()
        self.logger.debug("Exiting now")

    def run_once(self):
        """ Tries to pop a message or send an heartbeat
        """
        try:
            event = self.queue.get(timeout=self.sleep_delay)
            self.logger.debug('Run once, event: %s after %ss sleep delay', event, self.sleep_delay)
            self.handle_message(event)

            # Exit now if should stop
            if self.stop:
                return
        except Empty:
            self.logger.debug('No message after %ss sleep delay', self.sleep_delay)

        if self._should_do_heartbeat():
            self.do_heartbeat()

        # Aggregate observations in transit in observations queue
        self.aggregate_observations()

        if self._should_publish_metrics():
            self.publish_metrics()

        # Tick the deliverer to publish batch if necessary
        self.deliverer.tick()

    @property
    def sleep_delay(self):
        """ Compute the sleeping delay by taking the heartbeat and metrics delay
        minimum
        """
        return min([self.heartbeat_delay, self.publish_metrics_delay])

    def handle_message(self, event):
        """ Handle incoming message
        Process RunnerStop message or pass event to the deliverer
        """
        if event is RunnerStop:
            self.logger.debug('RunnerStop found, logout')
            self.logout()
            self.stop = True
        elif event is MetricsEvent:
            self.aggregate_observations()
        else:
            self.deliverer.post_event(event)

    def process_commands(self, commands):
        """ handle commands
        """
        while len(commands) > 0:
            result = self.remote_command.process_list(commands, self)
            result = self.session.post_commands_result(result)
            commands = result['commands']

    def do_heartbeat(self):
        """ Do an heartbeat
        """
        res = self.session.heartbeat()
        self.last_heartbeat_request = time()
        self._update_heartbeat_delay()
        self.process_commands(res['commands'])

    def publish_metrics(self):
        """ Publish finished metrics from MetricsStore
        """
        self.last_post_metrics_request = time()
        self.session.post_metrics(self.metrics_store.get_data_to_publish(datetime.utcnow()))

    def aggregate_observations(self):
        """ Empty the observation queue and update the metric store
        with the observations in the queue.
        """
        try:
            while True:
                observation = self.observation_queue.get_nowait()
                self.metrics_store.update(*observation)
        except Empty:
            pass

    def _update_heartbeat_delay(self):
        """ Update the heartbeat_delay if warmup period is finished
        """
        if time() - self.started > self.HEARTBEAT_WARMUP:
            self.heartbeat_delay = self.HEARTBEAT_MAX_DELAY

    def _should_do_heartbeat(self):
        """ Check if we should send an heartbeat because the delay is overdue
        """
        return (self.last_heartbeat_request + self.heartbeat_delay) < time()

    def _should_publish_metrics(self):
        """ Check if we should publish the metrics because the delay is overdue
        """
        return (self.last_post_metrics_request + self.publish_metrics_delay) < time()

    def logout(self):
        """ Run cleanup
        """
        self.logger.debug("Logout")

        # Flush metrics
        self.aggregate_observations()
        self.publish_metrics()

        # Drain deliverer
        self.deliverer.drain()

        self.session.logout()

    ###
    # Features
    ###

    def features_get(self):
        """ Returns the current values for all features switches
        """
        return {'publish_metrics_delay': self.publish_metrics_delay,
                'performance_metrics_period': self.performance_metrics_period,
                'batch_size': self.deliverer.batch_size,
                'max_staleness': self.deliverer.max_staleness,
                'call_counts_metrics_period': self.metrics_store.get_metric_period("sqreen_call_counts")}

    def set_publish_metrics_delay(self, new_metric_delay):
        """ Update the publish metrics delay
        """
        self.publish_metrics_delay = new_metric_delay

    def set_performance_metrics_period(self, new_performance_metrics_delay):
        self.performance_metrics_period = new_performance_metrics_delay

    def set_call_counts_metrics_period(self, call_counts_metrics_period):
        self.metrics_store.register_metric("sqreen_call_counts", "Sum",
                                           call_counts_metrics_period)

    def set_deliverer(self, batch_size, max_staleness):
        # Drain current deliverer
        self.deliverer.drain()

        # Replace current deliverer
        self.deliverer = get_deliverer(batch_size, max_staleness, self.session)

    def set_paths_whitelist(self, paths):
        """ Update current RunnerSettings paths_whitelist
        """
        self.logger.debug("Set paths whitelist on settings %r", self.settings)
        self.settings.paths_whitelist = paths
