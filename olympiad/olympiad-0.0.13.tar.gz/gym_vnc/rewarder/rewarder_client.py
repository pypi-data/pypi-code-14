import logging
from gym_vnc import pyprofile
import time
import ujson

from autobahn.twisted import websocket
from twisted.internet import defer

from gym_vnc import error, utils
from gym_vnc.rewarder import reward_buffer

logger = logging.getLogger(__name__)

class RemoteError(error.Error):
    pass

class RewarderClient(websocket.WebSocketClientProtocol):
    def __init__(self):
        super(RewarderClient, self).__init__()
        self._closed = False
        self._close_message = None

        self._connected = False
        self._requests = {}

    def reset_complete(self, initial=False):
        self.reward_buffer.push_info({'env_status.reset_complete': True})

    def onConnect(self, request):
        self._request_id = 0
        self._requests = {}

        self.reward_buffer = self.factory.reward_buffer

        self.factory.deferred.callback(self)
        # Make sure we don't accidentally try to double call it
        self.factory.deferred = None
        self._connected = True

    def send(self, method, body, headers=None, expect_reply=False):
        if headers is None:
            headers = {}
        if self._closed:
            error_message = "Can't send message to closed connection"
            if self._close_message:
                error_message += ": {}".format(self._close_message)
            e = error.Error(error_message)
            if expect_reply:
                d = defer.Deferred()
                d.errback(e)
                return d
            else:
                raise e

        id = self._request_id

        self._request_id += 1
        new_headers = {
            'request_id': id,
            'sent_at': time.time(),
        }
        new_headers.update(headers)

        payload = {
            'method': method,
            'body': body,
            'headers': new_headers,
        }

        logger.debug('Sending message to rewarder: %s', payload)
        self.sendMessage(ujson.dumps(payload).encode('utf-8'), False)

        if expect_reply:
            d = defer.Deferred()
            self._requests[id] = (payload, d)
            return d
        else:
            return None

    def recv(self, context, response):
        method = response['method']
        body = response['body']
        headers = response['headers']

        # Gets called by RewarderClient
        if method == 'env.reward':
            reward = body['reward']
            done = body['done']
            info = body['info']
            logger.debug('Received env.reward: reward=%s done=%s info=%s', reward, done, info)
            pyprofile.incr('rewarder_client.reward', reward)
            if done:
                pyprofile.incr('rewarder_client.done')
            # Make it possible for people to tell if the environment
            # has auto-reset yet.
            env_status = self.factory.env_status
            with env_status.cv:
                # We'll get an env.describe method shortly, but we
                # proactively change our state to resetting.
                if done:
                    env_status.set_env_info('resetting')
                _tag_env_status(info, env_status)
            self.reward_buffer.push(reward, done, info, headers['sent_at'], context['start'])
        elif method == 'env.text':
            text = body['text']
            logger.debug('Received env.texts: text=%s', text)
            self.reward_buffer.push_text(text)
        elif method == 'env.observation':
            jsonable = body['observation']
            logger.debug('Received env.observation: observation=%s', jsonable)
            self.reward_buffer.set_observation(jsonable)
        elif method == 'env.describe':
            env_id = body['env_id']
            env_state = body['env_state']
            env_instruction = body.get('env_instruction') # instructions for agent.

            logger.debug('Received env.describe: env_id=%s env_state=%s env_instruction=%s',
                         env_id, env_state, env_instruction)

            env_status = self.factory.env_status
            with env_status.cv:
                # Only consider it an update if the state actually
                # updated. Flashgames currently sends two env.describes
                # with env_state of running: one when the env actually
                # finishes, and one as the RPC reply.
                if env_state != env_status.env_state:
                    self.factory.env_status.set_env_info(env_state, env_id=env_id)
                info = {}
                _tag_env_status(info, env_status)
                # Needed so that mask knows that the state has changed
                self.reward_buffer.push_info(info)
        elif method in ['rpc.reply.error', 'rpc.reply.control.ping', 'rpc.reply.env.reset']:
            assert headers.get('parent_request_id') is not None
        elif method == 'connection.close':
            assert headers.get('parent_request_id') is None
            logger.debug('Server hanging up: %s', body['message'])
            self._close_message = body['message']
        else:
            logger.error('Unrecognized websocket method: method=%s body=%s headers=%s (consider adding to rewarder_state.py)', method, body, headers)
            return

        parent_id = headers.get('parent_request_id')
        if parent_id is not None:
            try:
                spec = self._requests.pop(parent_id)
            except KeyError:
                logger.error('Received extra reply to %d; ignoring: method=%s body=%s headers=%s ', parent_id, method, body, headers)
            else:
                request, d = spec
                if method != 'rpc.reply.error':
                    d.callback((context, request, response))
                else:
                    e = RemoteError('[{}] Remote error: {}'.format(self.factory.label, body['message']))
                    d.errback(e)

    def onMessage(self, payload, isBinary):
        logger.debug('Received payload: %s', payload)
        assert not isBinary
        payload = ujson.loads(payload)

        context = {'start': time.time()}
        latency = context['start'] - payload['headers']['sent_at']
        pyprofile.incr('rewarder_protocol.messages')
        pyprofile.incr('rewarder_protocol.messages.{}'.format(payload['method']))

        # Double latency to model RTT
        pyprofile.timing('rewarder_protocol.latency.rtt.skew_unadjusted', 2*latency)
        if latency < 0:
            pyprofile.incr('rewarder_protocol.latency.rtt.skew_unadjusted.negative')

        self.recv(context, payload)

    def onClose(self, wasClean, code, reason):
        if not self._connected:
            self.factory.deferred.errback(error.ConnectionError(reason))
            # Make sure we don't accidentally try to double call it
            self.factory.deferred = None
            return

        if not self._closed:
            error_message = '[{}] Lost connection: {} (clean={} code={})'.format(self.factory.label, reason, wasClean, code)
            reason = error.Error(error_message)
            # TODO: it's not an error if we requested it
            self.factory.record_error(reason)
        else:
            error_message = "In-flight message failed due to closed connection"
            if self._close_message:
                error_message += ": {}".format(self._close_message)
            reason = error.Error(error_message)

        for request, d in self._requests.values():
            d.errback(reason)

        self._closed = True

    def close(self):
        self._closed = True
        self.transport.loseConnection()

def _tag_env_status(info, env_status):
    # assumes a locked env_status
    info['env_status.episode_id'] = env_status._episode_id
    info['env_status.env_state'] = env_status._env_state
    info['env_status.state_id'] = env_status._state_id
    if env_status._metadata:
        info['env_status.instruction'] =  env_status._metadata.get('instruction', '')
