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


class NSClient(multiprocessing.Process):
    """Server process for net-survey."""

    UPDATING = 'updating'
    WAITING_DISTRIBUTION = 'waiting'
    DISCOVERY = 'discovery'
    SEND_RESULTS = 'results'
    FINISHED = 'finished'

    def __init__(self, conf, interfaces):
        multiprocessing.Process.__init__(self, name='netsurvey')
        self._conf = conf
        self._networks = interfaces.get_host_networks()
        self._state = self.UPDATING
        self._client = None
        self._server = None
        self._client_data = {}

    def run(self):
        """Main run process for Client."""
        logging.info('Starting Client Process: '
                     '%s with pid %s' % (self.name, self.pid))
        while True:
            if self._state == self.UPDATING and self._client is None:
                if self._send_data_to_server(self._networks):
                    logging.info('Networks sent: '
                                 'validated. Moving to %s.' %
                                 self.WAITING_DISTRIBUTION.upper())
                    self._state = self.WAITING_DISTRIBUTION
                else:
                    logging.debug('Sleeping for 10 Seconds')
                    time.sleep(10)
            elif self._state == self.WAITING_DISTRIBUTION:
                _received, _client_data = self._receive_data_from_server()
                if _received:
                    self._client_data.update(_client_data)
                    logging.info('Finished receiving distributed data. '
                                 'Moving to %s.' % self.DISCOVERY.upper())
                    self._state = self.DISCOVERY
            elif self._state == self.DISCOVERY:
                logging.debug('Discovery phase. Sleep 10.')
                time.sleep(10)

    def _terminate(self):
        """Terminate method for process.

        This will cleanup client connection and terminate the process.
        """
        if self._client is not None:
            logging.info('Shutting Down Client: '
                         '%s:%s' % (self._conf.server_ip,
                                    self._conf.server_port))
            self._client.close()
        logging.info('Stopping Client Process: '
                     '%s with pid %s' % (self.name, self.pid))
        sys.exit(0)

    def terminate(self, sig, func=None):
        """Terminate method for process.

        This will cleanup client connection and terminate the process.

        :param sig: signal object
        :param func: function object
        """
        self._terminate()

    def _send_data_to_server(self, data):
        """Send data to server.

        This will send the data to the server, i.e. networks or
        results.

        :returns True/False if data is validated/received from server
        """
        try:
            logging.debug('Sending data: (%s:%s) - '
                          '%s' % (self._conf.server_ip,
                                  self._conf.server_port,
                                  data))
            self._client = Client((self._conf.server_ip,
                                   self._conf.server_port))
            self._client.send(data)
            response = self._client.recv()
            if str(response) == 'validated':
                self._client.close()
                return True
        except Exception as e:
            logging.error('Unable to connect to server: '
                          '%s:%s - %s' % (self._conf.server_ip,
                                          self._conf.server_port,
                                          str(e)))
            return False
        finally:
            self._client = None

    def _receive_data_from_server(self):
        """Receive data from server.

        This method will retrieve the distributed data from the server.

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
                    logging.debug('Distributed data received from server: '
                                  '%s - Data: %s.' %
                                  (self._server.last_accepted[0],
                                   _client_data))
                    connection.send('validated')
                    connection.close()
                    self._server.close()
                    return True, _client_data
                except EOFError:
                    break
            connection.close()
