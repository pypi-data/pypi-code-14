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
from multiprocessing.connection import Client, Listener
import sys
import time


class NSServer(multiprocessing.Process):
    """Server process for net-survey."""

    LEARNING = 'learning'
    PROCESSING = 'processing'
    DISTRIBUTING = 'distributing'
    GATHERING = 'gathering'
    FINISHED = 'finished'

    def __init__(self, conf):
        multiprocessing.Process.__init__(self, name='netsurvey',)
        self._conf = conf
        self._state = self.LEARNING
        self._server = None
        self._client = None
        self._client_data = {}
        self._client_data['_host_detail'] = {}
        self._client_data['_networks'] = {}
        self._client_data['_clients'] = {}
        self._clients = self._populate_clients()
        logging.debug('Populated Inventory: %s' % self._clients)

    def run(self):
        """Main run process for Client."""
        # Remaining clients to distribute data to.
        _remaining_clients = []
        logging.info('Starting Server Process: '
                     '%s with pid %s' % (self.name, self.pid))
        while True:
            if self._state == self.LEARNING and self._server is None:
                _received, _client_data = self._receive_data_from_clients()
                if _received:
                    self._client_data['_host_detail'].update(_client_data)
                    logging.info('Finished receiving client data. '
                                 'Moving to %s.' % self.PROCESSING.upper())
                    self._state = self.PROCESSING
            elif self._state == self.PROCESSING:
                self._prepare_client_data()
                logging.debug('Client data prepared: %s' % self._client_data)
                logging.info('Moving to %s.' % self.DISTRIBUTING.upper())
                self._state = self.DISTRIBUTING
            elif self._state == self.DISTRIBUTING:
                _distributed, _remaining_clients = \
                    self._distribute_test_data(_remaining_clients)
                if _distributed:
                    logging.debug('Client data distributed: '
                                  '%s' % self._client_data)
                    logging.info('Moving to %s.' % self.GATHERING.upper())
                    self._state = self.GATHERING
                else:
                    logging.critical('Unable to distribute to clients. Trying '
                                     'again in 10 seconds. Clients in error: '
                                     '%s' % _remaining_clients)
                    time.sleep(10)

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
                     '%s:%s' % (self._conf.bind_host,
                                self._conf.bind_port))
        self._server = Listener((self._conf.bind_host,
                                 self._conf.bind_port))
        _client_data = None
        while True:
            connection = self._server.accept()
            while True:
                try:
                    _client_data = connection.recv()
                    logging.debug('Client data received from: '
                                  '%s - Data: %s.' %
                                  (self._server.last_accepted[0],
                                   _client_data))
                    # We update the _clients dict, adding the hostname
                    # to the ip key, if does not exist, we traverse the
                    # client_data looking for the ip.
                    self._update_clients(self._server.last_accepted[0],
                                         _client_data)
                except EOFError:
                    break
                connection.send('validated')
            connection.close()
            # Check the _clients dict to make sure we received all
            # client information.
            if self._check_clients():
                break
        self._server.close()
        return True, _client_data

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

    def _distribute_test_data(self, remaining_clients):

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
                                             self._client_data):
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
