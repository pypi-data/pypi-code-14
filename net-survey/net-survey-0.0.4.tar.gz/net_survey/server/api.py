"""
   Copyright 2016 Net-Survey

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import json
import logging
import multiprocessing
import re
import redis


class APIServer(multiprocessing.Process):

    def __init__(self, conf, redis_pool):
        multiprocessing.Process.__init__(self, name='apiserver',)
        self._conf = conf
        self._httpd_server = APIHTTPServer((self._conf.bind_host,
                                            self._conf.server_api_port),
                                           MainRequestHandler)
        self._httpd_server.set_redis_server(redis_pool)

    def run(self):
        logging.info('Starting API Process: '
                     '%s with pid %s' % (self.name, self.pid))
        try:
            logging.info('Starting API Server: %s:%s.' %
                         (self._conf.bind_host, self._conf.server_api_port))
            self._httpd_server.serve_forever()
        except Exception as e:
            logging.error('API Server Shutdown: %s:%s. Exception: %s' %
                          (self._conf.bind_host,
                           self._conf.server_api_port,
                           str(e)))
            self._terminate()

    def _terminate(self):
        """Terminate method for process.

        This will cleanup client connection and terminate the process.
        """
        logging.info('Shutting Down API Server: %s:%s' %
                     (self._conf.bind_host, self._conf.server_api_port))
        self._httpd_server.socket.close()
        logging.info('Stopping API Process: '
                     '%s with pid %s' % (self.name, self.pid))

    def terminate(self, sig, func=None):
        """Terminate method for process.

        This will cleanup client connection and terminate the process.

        :param sig: signal object
        :param func: function object
        """
        self._terminate()


class APIHTTPServer(HTTPServer):
    """HTTPServer Class to Set Queue and Event."""

    def set_redis_server(self, redis_pool):
        """Set Queue and Event Instances.

        :param redis_ip: redis server IP Address
        :param redis_port: redis server port
        """
        self.redis_pool = redis_pool


class Controller(object):
    """Controller Ref to Base Class."""

    def __init__(self, server):
        self.__server = server

    @property
    def server(self):
        """Ref to Base Class."""
        return self.__server


class Router(object):
    """Base Router."""

    def __init__(self, server):
        """Base Router.

        :param server: HTTPServer instance
        """
        self.__routes = []
        self.__server = server

    def addRoute(self, regexp, controller, action):
        """Add Route to Controller.

        :param regexp: regexp match on route
        :param controller: controller object
        :param action: controller action
        """
        self.__routes.append({'regexp': regexp,
                              'controller': controller,
                              'action': action})

    def route(self, path):
        """Check Route and Execute.

        :param path: URI Path
        """
        for route in self.__routes:
            if re.search(route['regexp'], path):
                cls = globals()[route['controller']]
                func = cls.__dict__[route['action']]
                obj = cls(self.__server)
                apply(func, (obj, ))
                return

        # 404 Not Found
        self.__server.send_response(404)
        self.__server.end_headers()


class MainRequestHandler(BaseHTTPRequestHandler):
    """Main Request Handler."""

    def __init__(self, request, client_address, server):

        self._redis_pool = server.redis_pool

        get_routes = [
            {'regexp': r'^/$',
             'controller': 'MainController',
             'action': 'indexAction'}
        ]

        post_routes = [
            {'regexp': r'^/start$',
             'controller': 'MainController',
             'action': 'scanAction'}
        ]

        self.__get_router = Router(self)
        self.__post_router = Router(self)

        for route in get_routes:
            self.__get_router.addRoute(route['regexp'],
                                       route['controller'],
                                       route['action'])

        for route in post_routes:
            self.__post_router.addRoute(route['regexp'],
                                        route['controller'],
                                        route['action'])

        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_GET(self):
        """Handle GETs."""
        self.__get_router.route(self.path)

    def do_POST(self):
        """Handle POSTs."""
        self.__post_router.route(self.path)


class MainController(Controller):
    """Main Controller."""

    START_SCAN = 'start_scan'

    def __init__(self, server):
        """Main Controller.

        :param server: HTTPServer instance
        """
        Controller.__init__(self, server)

    def _set_redis_action(self, action):
        """Sets the action on Redis action key.

        :param action: string action to set
        """
        if self.server._redis_pool is not None:
            try:
                r = redis.Redis(connection_pool=self.server._redis_pool)
                r.set('action', action)
            except Exception as e:
                logging.error('Unable to set action in Redis: %s' % str(e))
        else:
            logging.error('Redis connection not setup. Unable to set action.')

    def _get_redis_data(self):
        """Sets the action on Redis action key.

        :returns json object of scan data
        """
        if self.server._redis_pool is not None:
            try:
                r = redis.Redis(connection_pool=self.server._redis_pool)
                return json.loads(r.get('scan_data'))
            except Exception as e:
                logging.error('Unable to set action in Redis: %s' % str(e))
        else:
            logging.error('Redis connection not setup. Unable to set action.')

    def indexAction(self):
        """Handle GET to Index.

        This will set the event flag and wait for queue data.
        """
        _data = {}

        try:
            _data = self._get_redis_data()
        except Exception as e:
            logging.error('Unable to retrieve Redis scan data: %s' % str(e))

        self.server.send_response(200)
        self.server.send_header('Content-type', 'application/json')
        self.server.end_headers()
        # Write our data and clear the flag
        self.server.wfile.write(json.dumps(_data))

    def scanAction(self):
        """Handle POST to Index.

        This will start a scan.
        """
        _data = "OK"

        self._set_redis_action(self.START_SCAN)
        self.server.send_response(201)
        self.server.wfile.write(_data)
