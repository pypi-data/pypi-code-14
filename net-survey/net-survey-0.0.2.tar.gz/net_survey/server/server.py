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

import logging
import multiprocessing
from multiprocessing.connection import Client, SocketListener
from oslo_config import cfg
from oslo_config import types
import socket
import sys
import time

SecondsType = types.Integer(1, 5000)

netsurvey_server_opts = [
    cfg.Opt('listener_timeout',
            type=SecondsType,
            default=900,
            help='Number of seconds to wait for client connections.'),
    cfg.Opt('timeout_wait',
            type=SecondsType,
            default=30,
            help='Number of seconds to sleep after timeout.'),
    cfg.BoolOpt('scan_on_start',
                default=True,
                help='Start scan on server service start '
                     'True/False or yes/no.'),
]


class NSServer(multiprocessing.Process):
    """Server process for net-survey."""

    LEARNING = 'learning'
    PROCESSING = 'processing'
    DISTRIBUTING = 'distributing'
    GATHERING = 'gathering'
    FINISHED = 'finished'
    SLEEPING = 'sleeping'
    START_SCAN = 'start_scan'

    def __init__(self, queue, api_event, scan_event, conf):
        multiprocessing.Process.__init__(self, name='netsurvey',)
        self._queue = queue
        self._api_event = api_event
        self._scan_event = scan_event
        self._conf = conf
        self._register_server_opts(self._conf)
        self._server = None
        self._client = None
        self._initialize_data()
        if bool(conf.server.scan_on_start):
            self._state = self.START_SCAN

    def _initialize_data(self):
        """Initialize Data & Cleanup."""
        self._state = self.SLEEPING
        self._client_data = {}
        self._client_data['_state'] = self.SLEEPING
        self._client_data['_host_detail'] = {}
        self._client_data['_networks'] = {}
        self._client_data['_clients'] = {}
        self._clients = self._populate_clients()
        logging.debug('Populated Inventory: %s' % self._clients)

    def _register_server_opts(self, conf):
        """Register server options.

        :param conf: a ConfigOpts instance
        :raises: DuplicateOptError, ArgsAlreadyParsedError
        """
        conf.register_opts(netsurvey_server_opts, group='server')

    def run(self):
        """Main run process for Server."""

        # Remaining clients to distribute data to.
        _remaining_clients = []
        logging.info('Starting Server Process: '
                     '%s with pid %s' % (self.name, self.pid))
        while True:
            # Check if our API signalled an event
            self._check_api_event()
            # Learning State
            if self._state == self.LEARNING and self._server is None:
                _complete = self._receive_data_from_clients()
                if _complete:
                    logging.info('Finished receiving client data. '
                                 'Moving to %s.' % self.PROCESSING.upper())
                    self._state = self.PROCESSING
                    self._client_data['_state'] = self._state
                else:
                    logging.error('Waited a long time for all clients to '
                                  'report network data but timed out waiting. '
                                  'Check hosts: %s' %
                                  [ip for ip in self._clients.keys()
                                   if self._clients[ip] is None])
                    logging.debug('Sleeping for %s seconds.' %
                                  self._conf.server.timeout_wait)
                    time.sleep(self._conf.server.timeout_wait)
            # Processing State
            elif self._state == self.PROCESSING:
                self._prepare_client_data()
                logging.debug('Client data prepared: %s' % self._client_data)
                logging.info('Moving to %s.' % self.DISTRIBUTING.upper())
                self._state = self.DISTRIBUTING
                self._client_data['_state'] = self._state
            # Distribution State
            elif self._state == self.DISTRIBUTING:
                _distributed, _remaining_clients = \
                    self._distribute_data(_remaining_clients,
                                          self._client_data)
                if _distributed:
                    logging.debug('Client data distributed: '
                                  '%s' % self._client_data)
                    logging.info('Moving to %s.' % self.GATHERING.upper())
                    self._state = self.GATHERING
                    self._client_data['_state'] = self._state
                    # Setup clients dict for tracking again
                    self._clients = self._populate_clients()
                else:
                    logging.critical('Unable to distribute to clients. Trying '
                                     'again in %s seconds. Clients in error: '
                                     '%s' % (self._conf.server.timeout_wait,
                                             _remaining_clients))
                    time.sleep(self._conf.server.timeout_wait)
            # Gathering Results State
            elif self._state == self.GATHERING:
                _complete = self._receive_data_from_clients()
                if _complete:
                    logging.info('Finished receiving client data. '
                                 'Moving to %s.' % self.FINISHED.upper())
                    self._state = self.FINISHED
                    self._client_data['_state'] = self._state
                else:
                    logging.error('Waited a long time for all clients to '
                                  'report network data but timed out waiting. '
                                  'Check hosts: %s' %
                                  [ip for ip in self._clients.keys()
                                   if self._clients[ip] is None])
                    logging.debug('Sleeping for %s seconds.' %
                                  self._conf.server.timeout_wait)
                    time.sleep(self._conf.server.timeout_wait)
            elif self._state == self.FINISHED:
                logging.info('Finished Scanning.')
                logging.debug('Final client result data: %s' %
                              self._client_data)
                self._state = self.SLEEPING
                self._client_data['_state'] = self._state
            elif self._state == self.START_SCAN:
                _distributed, _remaining_clients = \
                    self._distribute_data(_remaining_clients,
                                          self.START_SCAN)
                if _distributed:
                    logging.debug('Client Initialized: '
                                  '%s' % self.START_SCAN.upper())
                    logging.info('Moving to %s.' % self.LEARNING.upper())
                    self._initialize_data()
                    self._state = self.LEARNING
                    self._client_data['_state'] = self._state
                else:
                    logging.critical('Unable to initialize clients. Trying '
                                     'again in %s seconds. Clients in error: '
                                     '%s' % (self._conf.server.timeout_wait,
                                             _remaining_clients))
                    time.sleep(self._conf.server.timeout_wait)
            elif self._state == self.SLEEPING:
                time.sleep(1)

    def _terminate(self):
        """Terminate method for process.

        This will cleanup client connection and terminate the process.
        """
        if self._server is not None:
            logging.info('Shutting Down Listener: '
                         '%s:%s' % (self._conf.bind_host,
                                    self._conf.bind_port))
            self._server.close()
        if self._client is not None:
            logging.info('Shutting Down Client.')
            self._client.close()
        logging.info('Stopping Server Process: '
                     '%s with pid %s' % (self.name, self.pid))
        sys.exit(0)

    def terminate(self, sig, func=None):
        """Terminate method for process.

        This will cleanup client connection and terminate the process.

        :param sig: signal object
        :param func: function object
        """
        self._terminate()

    def _receive_data_from_clients(self):
        """Receive data from clients.

        This method receives data from clients and returns true if data
        has been received.  If so, decision to transition to another state
        is done within the run() method.

        One check is made here, which is to check if data has been received
        from all clients in the states LEARNING and GATHERING.

        :returns bool(if data received), _client_data(dict of data received)
        """
        logging.info('Starting Listener: '
                     '%s:%s with Timeout: %s seconds' %
                     (self._conf.bind_host, self._conf.bind_port,
                      self._conf.server.listener_timeout))
        self._server = SocketListener((self._conf.bind_host,
                                       self._conf.bind_port), 'AF_INET')
        _complete = False
        while True:
            # Bypass Listener and use SocketListener to set timeout
            self._server._socket.settimeout(self._conf.server.listener_timeout)
            try:
                connection = self._server.accept()
            except socket.timeout:
                # Send us back to run() to communicate the timeout.
                break
            while True:
                try:
                    _recv_client_data = connection.recv()
                    logging.debug('Client data received from: '
                                  '%s - Data: %s.' %
                                  (self._server._last_accepted[0],
                                   _recv_client_data))
                    # We update the _clients dict, adding the hostname
                    # to the ip key, if does not exist, we traverse the
                    # client_data looking for the ip.
                    self._update_clients(self._server._last_accepted[0],
                                         _recv_client_data)
                    self._client_data['_host_detail'].update(_recv_client_data)
                    connection.send('validated')
                except EOFError:
                    break
            connection.close()
            # Check the _clients dict to make sure we received all
            # client information.
            if self._check_clients():
                _complete = True
                break
        self._server.close()
        self._server = None
        return _complete

    def _populate_clients(self):
        """Populate the _clients dict.

        :returns: dict of client ips in inventory file with empty hostname
        """
        client_file = open(self._conf.inventory_file, 'r')
        return {line.strip(): None
                for line in client_file.readlines()
                if '[' not in line}

    def _update_clients(self, host_ip, client_data):
        """Updates _clients dict with hostname of client."""
        try:
            for key in client_data.keys():
                self._clients[host_ip] = key
                logging.debug('Updated _client dict with hostname: %s.' % key)
        except KeyError as e:
            logging.debug('Unable to locate client ip in _clients dict. '
                          'We will now traverse client_data to find the '
                          'inventory ip address. %s' % str(e))

    def _check_clients(self):
        """Traverses the _clients dict to check completion.

        :returns: True/False if all client information has been received
        """
        _update_complete = True
        for value in self._clients.values():
            if value is None:
                _update_complete = False
        return _update_complete

    def _prepare_client_data(self):
        """Prepare data to be sent to the client for testing.

        A dict of networks and hostnames which have ips on the network are
        compiled as a key to retrieve ips to test against.

        { '_clients':
                'hostname: 'IP'
          '_networks':
                '10.0.0.0/24': ['host1', 'host2']
          '_host_detail':
                'hostname':
                    '10.0.0.1/24':
                        'ips': ['10.0.0.10' ,'10.0.0.2']
        }
        """

        # Loop through our networks for each host, determine if the network
        # has been added in the _networks key, if so just append the hostname
        # to the array.  If not, create they key and append.
        for _host in self._client_data['_host_detail'].keys():
            for _network in self._client_data['_host_detail'][_host].keys():
                if _network not in self._client_data['_networks'].keys():
                    self._client_data['_networks'][_network] = []
                self._client_data['_networks'][_network].append(_host)

        # Create a reverse dict of _clients for loopkup in the above network
        # reference.
        logging.debug('Processing clients: %s.' % self._clients)
        self._client_data['_clients'] = {self._clients[_host_ip]: _host_ip
                                         for _host_ip
                                         in self._clients.keys()}

    def _distribute_data(self, remaining_clients, data):
        """Iterates over a list of clients to distribute data to.

        List is compiled of unreachable clients for use on a retry.  If there
        are hosts in remaining_clients, the _clients dict is no longer used.

        :param remaining_clients: list of unreachable clients to
        distribute test data to.
        :param data: data to send to the client

        :returns: True/False if all client information has been sent, and
        a list of unreachable clients to use for a retry.
        """
        _distribute_to = []
        _errored_clients = []
        _distributed = True
        if len(remaining_clients) > 0:
            _distribute_to = remaining_clients
        else:
            _distribute_to = [_ip for _ip in self._clients.keys()]

        for _host_ip in _distribute_to:
            if not self._send_data_to_client(_host_ip,
                                             self._conf.bind_port,
                                             data):
                _errored_clients.append(_host_ip)
                _distributed = False

        return _distributed, _errored_clients

    def _send_data_to_client(self, client_ip, client_port, data):
        """Send data to server.

        This will send the finalized test data to the client.

        :returns True/False if data is validated/received from client
        """
        try:
            logging.debug('Sending data: (%s:%s) - '
                          '%s' % (client_ip, client_port, data))
            self._client = Client((client_ip, client_port))
            self._client.send(data)
            response = self._client.recv()
            if str(response) == 'validated':
                self._client.close()
                return True
        except Exception as e:
            logging.error('Unable to connect to client: '
                          '%s:%s - %s' % (client_ip,
                                          client_port,
                                          str(e)))
            return False
        finally:
            self._client = None

    def _check_api_event(self):
        """Check API Event Request."""
        if self._api_event.is_set():
            logging.debug('Received API Results Event.')
            self._queue.put(self._client_data)
            self._api_event.clear()

        if self._scan_event.is_set():
            logging.debug('Received API Scan Event.')
            self._state = self.START_SCAN
            self._client_data['_state'] = self._state
            self._scan_event.clear()
