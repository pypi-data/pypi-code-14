from autobahn.twisted import websocket
import logging
import numpy as np
import threading
import time

from twisted.python import failure
from twisted.internet import defer, endpoints, task
import twisted.internet.error

from gym_vnc import error, utils
from gym_vnc.twisty import reactor
from gym_vnc.rewarder import connection_timer, env_status, reward_buffer, rewarder_client
from gym_vnc.utils import display

logger = logging.getLogger(__name__)

def _ping(client):
    return client.send('rpc.control.ping', {}, expect_reply=True)

class RewarderSession(object):
    def __init__(self, start_timeout=None):
        self.lock = threading.Lock()

        self.i = 0

        # Mutated by main thread exclusively
        self.names_by_id = {}
        self.reward_buffers = {}
        self.env_statuses = {}
        self.errors = {}
        self.networks = {}

        self.clients = {}

        if start_timeout is None:
            start_timeout = 120
        self.start_timeout = start_timeout

    def close(self, name=None):
        if name is None:
            names = list(self.names_by_id.values())
        else:
            logger.info('Closing rewarder connection: %s', name)
            names = [name]
        self.ids_by_name = {name: id for id, name in self.names_by_id.items()}

        for name in names:
            with self.lock:
                id = self.ids_by_name.pop(name, None)
                if id is None:
                    # already closed
                    continue

                del self.names_by_id[id]
                del self.reward_buffers[id]
                del self.env_statuses[id]
                self.errors.pop(id, None)

                network = self.networks.pop(id)
                network.close()

                client = self.clients.pop(id, None)
                if client is not None:
                    reactor.callFromThread(client.close)

    def connect(self, name, address, env_id=None, seed=None, fps=60):
        if name in self.reward_buffers:
            self.close(name)

        label = 'rewarder:{}:{}:{}'.format(self.i, name, address)

        network = Network()
        self.names_by_id[self.i] = name
        self.reward_buffers[self.i] = reward_buffer.RewardBuffer()
        self.env_statuses[self.i] = env_status.EnvStatus(label)
        self.networks[self.i] = network

        reactor.callFromThread(self._connect, name,
                               address, env_id, seed, fps,
                               i=self.i, network=network,
                               env_status=self.env_statuses[self.i],
                               reward_buffer=self.reward_buffers[self.i],
                               label=label,
                               max_sleep_time=self.start_timeout,
        )
        self.i += 1
        return network

    # Call only from Twisted thread

    def _connect(self, name, address, env_id, seed, fps, i, network, env_status, reward_buffer,
                 label,
                 attempt=0, elapsed_sleep_time=0, max_sleep_time=None,
    ):
        endpoint = endpoints.clientFromString(reactor, 'tcp:'+address)
        factory = websocket.WebSocketClientFactory('ws://'+address)
        factory.protocol = rewarder_client.RewarderClient
        factory.i = i

        # Various important objects
        factory.endpoint = endpoint
        factory.env_status = env_status
        factory.reward_buffer = reward_buffer

        # Helpful strings
        factory.label = label
        factory.address = address

        # Arguments to always send to the remote reset call
        factory.arg_env_id = env_id
        factory.arg_fps = fps

        def record_error(e):
            if isinstance(e, failure.Failure):
                e = e.value

            # logger.error('[%s] Recording rewarder error: %s', factory.label, e)
            with self.lock:
                # drop error on the floor if we're already closed
                if factory.i in self.names_by_id:
                    self.errors[factory.i] = e
        factory.record_error = record_error

        def websocket_failed(reason):
            # Also need to handle DNS errors, so let's just handle everything for now.
            #
            # reason.trap(twisted.internet.error.ConnectError, error.ConnectionError)
            if elapsed_sleep_time < max_sleep_time:
                sleep = min((2 * attempt+1), 10)
                logger.error('[%s] %s. Going to retry in %ds (slept %ds/%ds): %s', factory.label, websocket_failed.error_message, sleep, elapsed_sleep_time, max_sleep_time, reason.value)
                reactor.callLater(sleep, self._connect, name, address, env_id, seed, fps, i, network, env_status, reward_buffer, label, attempt+1, elapsed_sleep_time+sleep, max_sleep_time)
            else:
                logger.error('[%s] %s. Retries exceeded (slept %ds/%ds): %s', factory.label, websocket_failed.error_message, elapsed_sleep_time, max_sleep_time, reason.value)
                factory.record_error(reason)

        def fail(reason):
            factory.record_error(reason)

        def connected(client):
            logger.info('[%s] Websocket client successfully connected', factory.label)

            # Websocket client has come up fully. Time to start on the
            # next level of our callback chain. (There must be a
            # better way to write this.)
            def calibrate_success(network):
                logger.info('[%s] Network calibration complete', factory.label)

                def reset_success(reply):
                    # We're connected and have measured the
                    # network. Mark everything as ready to go.
                    with self.lock:
                        if factory.i not in self.names_by_id:
                            # ID has been popped!
                            logger.info('[%s] Rewarder started, but has already been closed', factory.label)
                            client.close()
                        else:
                            logger.info('[%s] Rewarder came up successfully', factory.label)
                        self.clients[factory.i] = client
                    client.reset_complete(True)

                if factory.arg_env_id is not None:
                    d = self._send_env_reset(client, seed=seed)
                    d.addCallback(reset_success)
                    d.addErrback(fail)
                else:
                    # No env_id requested, so we just proceed without a reset
                    reset_success(None)

            d = network.calibrate(client)
            d.addCallback(calibrate_success)
            websocket_failed.error_message = 'WebSocket handshake established but calibration failed'
            d.addErrback(websocket_failed)
            d.addErrback(fail)

        d = defer.Deferred()
        d.addCallbacks(connected)
        websocket_failed.error_message = 'TCP connection established but WebSocket handshake failed'
        d.addErrback(websocket_failed)
        d.addErrback(fail)
        factory.deferred = d

        def connection_succeeded(conn):
            logger.info('[%s] Rewarder TCP connection established', factory.label)
        def connection_failed(reason):
            reason = error.Error('[{}] Connection failed: {}'.format(factory.label, reason.value))

            try:
                d.errback(utils.format_error(reason))
            except defer.AlreadyCalledError:
                raise
        res = endpoint.connect(factory)
        res.addCallback(connection_succeeded)
        websocket_failed.error_message = 'Could not establish rewarder TCP connection'
        res.addErrback(websocket_failed)
        res.addErrback(connection_failed)

    def pop_errors(self):
        errors = {}
        with self.lock:
            if self.errors:
                for i, error in self.errors.items():
                    name = self.names_by_id[i]
                    errors[name] = error
                self.errors.clear()
        return errors

    def reset(self):
        reactor.callFromThread(self._reset)

    def _reset(self):
        with self.lock:
            for client in self.clients.values():
                d = self._send_env_reset(client)
                # Total hack to capture the variable in the closure
                def callbacks(client):
                    def success(reply): client.reset_complete()
                    def fail(reason): client.factory.record_error(reason)
                    return success, fail
                success, fail = callbacks(client)
                d.addCallback(success)
                d.addErrback(fail)

    def _send_env_reset(self, client, seed=None):
        logger.info('[%s] Sending reset for env_id=%s fps=%s', client.factory.label, client.factory.arg_env_id, client.factory.arg_fps)
        d = client.send('rpc.env.reset', {
            'seed': seed,
            'env_id': client.factory.arg_env_id,
            'fps': client.factory.arg_fps,
        }, expect_reply=True)

        def success(reply):
            # clear any accumulated rewards
            reward, done, info = client.reward_buffer.pop()
            if info['reward.count'] > 0:
                logger.info('[%s] Dropping %d rewards from before the environment reset', client.factory.label, info['reward.count'])
            return reply
        def fail(reason):
            client.factory.record_error(reason)

        d.addCallback(success)
        d.addErrback(fail)
        return d

    def pop(self, warn=True):
        reward_d = {}
        done_d = {}
        info_d = {}
        err_d = self.pop_errors()

        for i, reward_buffer in self.reward_buffers.items():
            name = self.names_by_id[i]

            reward, done, info = reward_buffer.pop()
            reward_d[name] = reward
            done_d[name] = done
            info_d[name] = info

        if warn and any(info['reward.count'] > 10 for info in info_d.values()):
            logger.warn('WARNING: returning more than 10 aggregated rewards: %s. Either your agent is not keeping up with the framerate, or you should have called ".reset()" to clear pending rewards and reset the environments to a known state.', {name: str(info['reward.count']) for name, info in info_d.items()})

        return reward_d, done_d, info_d, err_d

    def wait(self, timeout=None):
        deadline = time.time() + timeout
        for client in self._clients:
            if timeout is not None:
                remaining_timeout = deadline - time.time()
            else:
                remaining_timeout = None
            client.reward_buffer.wait_for_step(timeout=remaining_timeout)

    # Hack to test actions over websockets
    # TODO: Carve websockets out of rewarder pkg (into vnc_env? - and move this there)
    def send_action(self, action, env_id):
        body = {
            'env_id': env_id,
            'action': action,
        }
        utils.blockingCallFromThread(self._send_action, body)

    def _send_action(self, *a, **kw):
        for client in self._clients:
            client.send('rpc.agent.action', a[0], expect_reply=False)

    def rewards_count(self):
        # TODO: any reason to lock these?
        return [client.reward_buffer.count for client in self._clients]

    def pop_observation(self):
        return [client.reward_buffer.pop_observation() for client in self._clients]

    # def _connection_time(self):
    #     deferreds = []
    #     for client in self._clients:
    #         endpoint = client.factory.endpoint
    #         d = connection_timer.start(endpoint)
    #         deferreds.append(d)

    #     d = defer.DeferredList(deferreds, fireOnOneErrback=True, consumeErrors=True)
    #     return d

# Run this in Twisty therad
class Network(object):
    def __init__(self):
        self.connection_samples = 10
        self.application_ping_samples = 10

        self.connection_time_m = None
        self.lock = threading.Lock()

        self.recalibrate = None
        self.client = None

        self._ntpdate_reversed_clock_skew = None
        self._reversed_clock_skew = None

        # self.clock_skew_strategy = clock_skew_strategy

    def active(self):
        with self.lock:
            return self._reversed_clock_skew is not None

    # Used by external consumers
    def reversed_clock_skew(self):
        with self.lock:
            if self._ntpdate_clock_skew is not None:
                return self._ntpdate_reversed_clock_skew
            else:
                return self._reversed_clock_skew

    def _report(self):
        connection_time = display.display_timestamps(self.connection_time_m)
        if self._ntpdate_clock_skew is not None:
            ntpdate_clock_skew = display.display_timestamp(self._ntpdate_clock_skew[0])
        else:
            ntpdate_clock_skew = None
        clock_skew = display.display_timestamps_pair(self.clock_skew_m)
        application_rtt = display.display_timestamps(self.application_rtt_m)
        request_overhead = display.display_timestamps(self.request_overhead_m)
        response_overhead = display.display_timestamps(self.response_overhead_m)

        logger.info('[%s] Network calibration: ntpdate_clock_skew=%s clock_skew=%s connection_time=%s application_rtt=%s request_overhead=%s response_overhead=%s',
                    self.client.factory.label, ntpdate_clock_skew, clock_skew, connection_time, application_rtt,
                    request_overhead, response_overhead)

    def _start(self):
        def calibrate():
            d = defer.Deferred()
            def fail(reason):
                logger.error('[%s] Could not recalibrate network: %s', self.client.factory.label, reason)
            d.addErrback(fail)
            self._start_measure_connection_time(d)
            self._start()
        self.recalibrate = reactor.callLater(5 * 60, calibrate)

    def close(self):
        if self.recalibrate:
            try:
                self.recalibrate.cancel()
            except twisted.internet.error.AlreadyCalled:
                pass

    # Called externally
    def calibrate(self, client):
        d = defer.Deferred()
        def success(res):
            # If we succeed, kick off the periodic 5 minute
            # recalibrations.
            self._start()
            return res
        d.addCallback(success)

        self.client = client

        # Kinda a hack. Idea is to try using the ntpdate -q offset if
        # we can.
        skew = self._start_measure_clock_skew()
        def succeed(offset):
            with self.lock:
                self._ntpdate_clock_skew = np.array([offset, offset])
                self._ntpdate_reversed_clock_skew = np.array([-offset, -offset])
            self._start_measure_connection_time(d)
        skew.addCallback(succeed)

        def fail(reason):
            with self.lock:
                self._ntpdate_clock_skew = None
                self._ntpdate_reversed_clock_skew = None

            logger.info('[%s] Could not determine clock skew with ntpdate; falling back to application-level ping: %s', self.client.factory.label, reason.value)
            self._start_measure_connection_time(d)
        skew.addErrback(fail)

        return d

    def _start_measure_connection_time(self, d):
        connection_time_m = np.zeros(self.connection_samples)
        self._measure_connection_time(d, connection_time_m, 0)

    def _measure_connection_time(self, d, connection_time_m, i):
        logger.debug('[%s] Measuring connection time (%d/%d)', self.client.factory.label, i+1, len(connection_time_m))
        endpoint = self.client.factory.endpoint
        timer = connection_timer.start(endpoint)

        def success(delta):
            connection_time_m[i] = delta
            if i+1 < len(connection_time_m):
                self._measure_connection_time(d, connection_time_m, i+1)
            else:
                self.connection_time_m = connection_time_m
                self._start_measure_application_ping(d)
        def fail(reason):
            d.errback(reason)
        timer.addCallback(success)
        timer.addErrback(fail)

    def _start_measure_application_ping(self, d=None):
        clock_skew_m = np.zeros((self.application_ping_samples, 2))
        request_overhead_m = np.zeros((self.application_ping_samples))
        response_overhead_m = np.zeros((self.application_ping_samples))
        application_rtt_m = np.zeros((self.application_ping_samples))

        self._measure_application_ping(d, clock_skew_m, request_overhead_m, response_overhead_m, application_rtt_m, 0)

    def _measure_application_ping(self, d, clock_skew_m, request_overhead_m, response_overhead_m, application_rtt_m, i):
        logger.debug('[%s] Issuing an application-level ping (%d/%d)', self.client.factory.label, i+1, len(clock_skew_m))
        start = time.time()
        ping = _ping(self.client)

        def success(res):
            context, request, response = res
            end = time.time()

            request_sent_at = request['headers']['sent_at'] # local
            response_sent_at = response['headers']['sent_at'] # remote
            response_received_at = context['start'] # local

            # We try to put bounds on clock skew by subtracting
            # local and remote times, for local and remote events
            # that are causally related.
            #
            # For example, suppose that the following local/remote
            # logical timestamps apply to a request (for a system
            # with clock skew of 100):
            #
            # request_sent       local: 0   remote: 100
            # request_recieved   local: 1   remote: 101
            # response_sent      local: 2   remote: 102
            # response_received  local: 3   remote: 103
            #
            # Then:
            #
            # # Remote event *after* local is upper bound
            # request_recieved.remote - request_sent.local = 101
            # # Remote event *before* local is lower bound
            # response_sent.remote - response_received.local = 102 - 3 = 99
            #
            # There's danger of further clock drift over time, but
            # we don't need these to be fully accurate, and this
            # should be fine for now.
            clock_skew_m[i, :] = (response_sent_at-response_received_at, response_sent_at-request_sent_at)
            request_overhead_m[i] = request_sent_at - start
            response_overhead_m[i] = end - response_received_at
            application_rtt_m[i] = response_received_at - request_sent_at

            if i+1 < len(clock_skew_m):
                self._measure_application_ping(d, clock_skew_m, request_overhead_m, response_overhead_m, application_rtt_m, i+1)
            else:
                self.clock_skew_m = clock_skew_m
                self.request_overhead_m = request_overhead_m
                self.response_overhead_m = response_overhead_m
                self.application_rtt_m = application_rtt_m

                self._report()
                self._update_exposed_metrics()

                # Ok, all done!
                if d is not None:
                    d.callback(self)
        def fail(reason):
            d.errback(reason)
        ping.addCallback(success)
        ping.addErrback(fail)

    def _update_exposed_metrics(self):
        with self.lock:
            self._clock_skew = self.clock_skew_m.mean(axis=0) # add to local time to get remote time, as (min, max) values
            self._reversed_clock_skew = -self._clock_skew[[1, 0]] # add to remote time to get local time, in format (min, max)


    def _start_measure_clock_skew(self):
        host = self.client.factory.address.split(':')[0]
        return connection_timer.measure_clock_skew(self.client.factory.label, host)
