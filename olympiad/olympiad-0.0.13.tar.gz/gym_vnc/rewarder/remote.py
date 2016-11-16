import logging
from gym_vnc import pyprofile
import sys
is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as queue
else:
    import queue as queue
import threading
import time
import ujson
import collections

from autobahn.twisted import websocket
from gym_vnc.twisty import reactor

logger = logging.getLogger(__name__)

class RewarderProtocol(websocket.WebSocketServerProtocol):
    connections = None

    def onConnect(self, request):
        logger.info('Client connecting: %s', request.peer)
        self.request = request
        self._request_id = 0

    def onOpen(self):
        logger.info('WebSocket connection established')
        self.factory.agent_conn._register(self)

        env_status = self.factory.agent_conn.env_status
        self.factory.agent_conn.send_env_describe(env_status.env_id, env_status.env_state)

    def onMessage(self, payload, isBinary):
        self.factory.agent_conn._incr_messages(self)

        assert not isBinary
        payload = ujson.loads(payload)

        context = {
            'start': time.time(),
            'conn': self,
        }
        latency = context['start'] - payload['headers']['sent_at']
        pyprofile.incr('rewarder_protocol.messages')
        pyprofile.incr('rewarder_protocol.messages.{}'.format(payload['method']))

        pyprofile.timing('rewarder_protocol.latency.rtt.skew_unadjusted', 2*latency)
        if latency < 0:
            pyprofile.incr('rewarder_protocol.latency.rtt.skew_unadjusted.negative')

        if payload['method'] == 'rpc.env.reset':
            logger.info('Received reset message: %s', payload)
            self.factory.agent_conn.control_buffer.recv_rpc(context, payload)
        elif payload['method'] == 'rpc.control.ping':
            logger.debug('Received ping message: %s', payload)
            parent_request_id = payload['headers']['request_id']
            headers = {'parent_request_id': parent_request_id}
            self.send_message('rpc.reply.control.ping', {}, headers)
            self._save_liveness()

    def _save_liveness(self):
        """ Write last received ping timestamp to /tmp
        To be used as kubernetes liveness check """
        with open('/tmp/gym-vnc-liveness', 'w') as f:
            f.write(str(time.time()))

    def onClose(self, wasClean, code, reason):
        logger.info('WebSocket connection closed: %s', reason)
        self.factory.agent_conn._unregister(self)

    def send_message(self, method, body, headers):
        id = self._request_id

        self._request_id += 1
        new_headers = {
            'request_id': id,
            'sent_at': time.time(),
        }
        if headers:
            new_headers.update(headers)

        payload = {
            'method': method,
            'body': body,
            'headers': new_headers,
        }

        # TODO: clean this up. Right now we decide whether it's info
        # or debug depending on whether it's a reply message.
        if 'parent_request_id' in new_headers and method != 'rpc.reply.control.ping':
            logger.info('Sending rewarder message: %s', payload)
        else:
            logger.debug('Sending rewarder message: %s', payload)

        self.sendMessage(ujson.dumps(payload).encode('utf-8'), False)

class ControlBuffer(object):
    def __init__(self):
        self.buf = queue.Queue()

    def recv_rpc(self, context, payload):
        """Call from any thread"""
        self.buf.put(('rpc', (context, payload)))

    def client_disconnect(self, conn, stats):
        self.buf.put(('client_disconnect', (conn, stats)))

    def get(self, *args, **kwargs):
        """Call from main thread."""
        return self.buf.get(*args, **kwargs)

class AgentConn(object):
    def __init__(self, env_status, cv, control_buffer, exclusive=False):
        self.env_status = env_status
        self.control_buffer = control_buffer
        self.cv = cv

        self.conns = {}

        self.exclusive = exclusive

        self._current_observation = None

    def active_clients(self):
        return [conn for conn, stats in self.conns.items() if stats['messages'] > 0]

    def listen(self, port=15900):
        logger.info('Starting Rewarder on port=%s', port)
        factory = websocket.WebSocketServerFactory()
        factory.agent_conn = self
        factory.protocol = RewarderProtocol

        reactor.callFromThread(reactor.listenTCP, port, factory)

    def _incr_messages(self, conn):
        with self.cv:
            self.conns[conn]['messages'] += 1

    def _register(self, conn):
        with self.cv:
            # Note: if this exceptions, Autobahn will end up capturing
            # the errors since its hooks are called via
            # maybeDeferred. This won't always print the prettiest
            # stack trace.
            if self.exclusive and any(c['messages'] > 0 for c in self.conns.values()):
                # Already full up, sorry!
                logger.info('Dropping new connection since there is already a client')
                conn.send_message('connection.close', {'message': 'The server is operating in exclusive mode and already has a client.'}, {})
                conn.transport.loseConnection()
                return

            self.conns[conn] = {'messages': 0}
            self.cv.notifyAll()

        if self._current_observation:
            self._send_env_observation(self._current_observation, conn)

    def _unregister(self, conn):
        with self.cv:
            try:
                stats = self.conns[conn]
            except KeyError:
                stats = None
            else:
                self.cv.notifyAll()

            self.control_buffer.client_disconnect(conn, stats)
            self.conns.pop(conn, None)  # Remove the connection from AgentConn

    def _broadcast(self, method, body, headers=None, conn=None):
        if conn:
            conns = [conn]
        else:
            conns = self.conns

        for conn in conns:
            conn.send_message(method, body, headers)

    def send_env_text(self, text):
        ''' text channel to communicate with the agent '''
        reactor.callFromThread(self._send_env_text, text)

    def _send_env_text(self, text):
        self._broadcast('env.text', {
            'text': text
        })

    def send_env_observation(self, observation):
        reactor.callFromThread(self._send_env_observation, observation)

    def _send_env_observation(self, observation, conn=None):
        self._current_observation = observation

        self._broadcast('env.observation', {
            'observation': observation,
        }, conn=conn)

    def send_env_reward(self, reward, done, info):
        pyprofile.incr('agent_conn.reward', reward)
        if done:
            pyprofile.incr('agent_conn.done')

        reactor.callFromThread(self._send_env_reward, reward, done, info)

    def _send_env_reward(self, reward, done, info):
        self._broadcast('env.reward', {
            'reward': reward,
            'done': done,
            'info': info,
        })

    def send_env_describe(self, *args, **kwargs):
        reactor.callFromThread(self._send_env_describe, *args, **kwargs)

    def _send_env_describe(self, env_id, env_state, headers=None, parent_request_id=None, parent_context=None):
        conn = None
        if headers is None:
            headers = {}

        if parent_request_id is not None:
            headers['parent_request_id'] = parent_request_id
            headers['parent_runtime'] = time.time() - parent_context['start']
            conn = parent_context['conn']

        # TODO: decide how to handle multiple concurrent envs
        self._broadcast('env.describe', {
            'env_id': env_id,
            'env_state': env_state
        }, headers, conn)

    def send_rpc_reply_error(self, *args, **kwargs):
        reactor.callFromThread(self._send_rpc_reply_error, *args, **kwargs)

    def _send_rpc_reply_error(self, message, parent_request_id, parent_context):
        headers = {}
        headers['parent_request_id'] = parent_request_id
        headers['parent_runtime'] = time.time() - parent_context['start']
        conn = parent_context['conn']

        # TODO: decide how to handle multiple concurrent envs
        self._broadcast('rpc.reply.error', {
            'message': message,
        }, headers, conn)
