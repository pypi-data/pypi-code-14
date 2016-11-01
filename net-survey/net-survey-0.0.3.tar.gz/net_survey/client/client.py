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
from platform import node
from Queue import Queue
from scanner import NetworkScanner
import socket
import sys
import time

SecondsType = types.Integer(1, 5000)
IntType = types.Integer(1, 50)

netsurvey_client_opts = [
    cfg.Opt('listener_timeout',
            type=SecondsType,
            default=900,
            help='Number of seconds to wait for client connections.'),
    cfg.Opt('timeout_wait',
            type=SecondsType,
            default=30,
            help='Number of seconds to sleep after timeout.'),
    cfg.Opt('scan_timeout',
            type=SecondsType,
            default=2,
            help='Number of seconds timeout for scan.'),
    cfg.StrOpt('scan_ports',
               default='1-1024',
               help='Ports to scan, i.e. 1-1024,9000,9696'),
    cfg.StrOpt('critical_ports',
               help='Ports neighboring hosts should be able to reach, and if '
                    'not, alert. This port must be in the scan_ports range.'),
    cfg.StrOpt('fake_ports',
               help='Ports this host should open a listener on, usually to '
                    'facilitate testing of critical ports where a service '
                    'is not actively running.'),
    cfg.Opt('concurrent_scans',
            type=IntType,
            default=1,
            help='Number of concurrent scans.'),
]


class NSClient(multiprocessing.Process):
    """Client process for net-survey."""

    UPDATING = 'updating'
    WAITING_DISTRIBUTION = 'awaiting_distribution'
    DISCOVERY = 'discovery'
    SEND_RESULTS = 'send_results'
    FINISHED = 'finished'
    SLEEPING = 'sleeping'
    SCAN_SUCCESSFUL = 'success'
    SCAN_FAILED = 'failed'
    START_SCAN = 'start_scan'

    def __init__(self, conf, interfaces):
        multiprocessing.Process.__init__(self, name='netsurvey')
        self._conf = conf
        self._interfaces = interfaces
        self._register_client_opts(self._conf)
        self._hostname = node()
        self._initialize_data()
        self._client = None
        self._server = None

    def _initialize_data(self):
        """Initialize Data & Cleanup."""
        self._networks = self._interfaces.get_host_networks()
        self._initialize_networks()
        self._state = self.SLEEPING
        self._client_data = {}
        self._result_data = {
            self._hostname: {}
        }
        self._ips_to_networks = {}
        self._ips_to_hostname = {}

    def _register_client_opts(self, conf):
        """Register server options.

        :param conf: a ConfigOpts instance
        :raises: DuplicateOptError, ArgsAlreadyParsedError
        """
        conf.register_opts(netsurvey_client_opts, group='client')

    def run(self):
        """Main run process for Client."""
        logging.info('Starting Client Process: '
                     '%s with pid %s' % (self.name, self.pid))
        while True:
            # Updating State
            if self._state == self.UPDATING and self._client is None:
                if self._send_data_to_server(self._networks):
                    logging.info('Networks sent: '
                                 'validated. Moving to %s.' %
                                 self.WAITING_DISTRIBUTION.upper())
                    self._state = self.WAITING_DISTRIBUTION
                else:
                    logging.debug('Sleeping for %s Seconds.' %
                                  self._conf.client.timeout_wait)
                    time.sleep(self._conf.client.timeout_wait)
            # Awaiting Distribution State
            elif self._state == self.WAITING_DISTRIBUTION:
                _received, _client_data = self._receive_data_from_server()
                if _received:
                    self._client_data.update(_client_data)
                    logging.info('Finished receiving distributed data. '
                                 'Moving to %s.' % self.DISCOVERY.upper())
                    self._state = self.DISCOVERY
                else:
                    logging.error('Waited a long time for the server to '
                                  'distribute data, closing and waiting.')
                    logging.debug('Sleeping for %s seconds.' %
                                  self._conf.client.timeout_wait)
                    time.sleep(self._conf.client.timeout_wait)
            # Discovery State
            elif self._state == self.DISCOVERY:
                _ports_to_scan = \
                    self._parse_ports(self._conf.client.scan_ports)
                _ips_to_scan = self._prepare_thread_ips(self._client_data)
                logging.debug('Ready to perform scans against ips: '
                              '%s' % _ips_to_scan)
                logging.debug('Scanning ports: %s' % _ports_to_scan)
                if not len(_ips_to_scan) > 0:
                    logging.warning('No neighboring hosts to scan. Shutting '
                                    'down process.')
                    self._terminate()
                else:
                    self._scan_ips(_ips_to_scan, _ports_to_scan,
                                   self._conf.client.concurrent_scans)
                    logging.debug('Scan Complete! Moving to %s.' %
                                  self.SEND_RESULTS.upper())
                    self._state = self.SEND_RESULTS
            elif self._state == self.SEND_RESULTS:
                logging.debug('Sending Results.')
                if self._send_data_to_server(self._result_data):
                    logging.info('Results sent: '
                                 'validated. Moving to %s.' %
                                 self.FINISHED.upper())
                    self._state = self.FINISHED
                else:
                    logging.debug('Sleeping for %s Seconds.' %
                                  self._conf.client.timeout_wait)
                    time.sleep(self._conf.client.timeout_wait)
            elif self._state == self.FINISHED:
                logging.info('Finished Scanning.')
                self._state = self.SLEEPING
            elif self._state == self.SLEEPING:
                _received, _command = self._receive_data_from_server()
                if _received and self.START_SCAN in str(_command):
                    logging.info('Received command from server to scan. '
                                 'Moving to %s.' % self.UPDATING.upper())
                    self._initialize_data()
                    self._state = self.UPDATING
                else:
                    logging.info('Waited a long time for the server to '
                                 'give a command, closing and waiting.')
                    logging.debug('Sleeping for %s seconds.' %
                                  self._conf.client.timeout_wait)
                    time.sleep(self._conf.client.timeout_wait)

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

    def _initialize_networks(self):
        """Adds results key & populates critical ports."""
        _critical_ports = {
            'critical_ports':
                self._parse_ports(self._conf.client.critical_ports)
        }
        for _network in self._networks[self._hostname]:
            self._networks[self._hostname][_network]['results'] = {}
            self._networks[self._hostname][_network].update(_critical_ports)

    def _parse_ports(self, ports):
        """Parse a config string of ports to scan.

        The config param is only allow '-' and ',' as separators, but will
        convert the string to an array of ports to scan.

        :param ports: config str of ports to scan
        :raises: TypeError

        :returns list of ports to scan from string of ports
        """
        _scan_ports = []

        if ports is not None:
            _str_ports_array = ports.split(',')

            for str_port in _str_ports_array:
                if '-' in str_port:
                    _start_port = int(str_port.split('-')[0])
                    _end_port = int(str_port.split('-')[-1])
                    for _port in range(_start_port, _end_port):
                        _scan_ports.append(_port)
                else:
                    _scan_ports.append(int(str_port))

        return _scan_ports

    def _prepare_thread_ips(self, client_data):
        """Prepare a list of ips this host needs to scan

        Scan through our own networks that we have connected and grab a list
        of neighboring hosts who have the same network.  If the host in that
        list does not equal our own hostname, go ahead and append the IP
        Addresses to a list of ips available for threads to scan.

        :param client_data: dict of prepared data to perform scans against
        :returns list of ips to scan
        """
        _scan_ips = []

        for _network in client_data['_host_detail'][self._hostname].keys():
            for _host in client_data['_networks'][_network]:
                if _host != self._hostname:
                    ips = client_data['_host_detail'][_host][_network]['ips']
                    if len(ips) > 0:
                        for ip in ips:
                            _scan_ips.append(ip)
                            # Need to keep a relationship of ips to networks
                            # and host for posting results.
                            self._ips_to_networks[ip] = _network
                            self._ips_to_hostname[ip] = _host

        return _scan_ips

    def _scan_ips(self, _ips, _ports, _concurrent_scans):
        """Perform scan on neighboring IP Addresses

        Setup queues and threads per IP and consume the concurrent_threads
        configuration to determine how many will be scanning at one time.

        State list will keep track of all threads and their two states:
        scanning and hold_scan. It's important to pause after sending then
        scan command to the queue, as it will take at most 1 second for the
        thread to consume it.

        :param _ips: list of ips to scan
        :param _ports: list of ports to scan
        :param _concurrent_scans: int number of concurrent scans
        """
        _num_threads = len(_ips)
        _queues = [x for x in range(0, _num_threads)]
        _threads = [x for x in range(0, _num_threads)]
        _start_events = [x for x in range(0, _num_threads)]
        _stop_events = [x for x in range(0, _num_threads)]
        _ip_scanned_ports = {ip: [] for ip in _ips}

        # Setup queues, threads, and events
        for x in range(0, _num_threads):
            _queues[x] = Queue()
            _start_events[x] = multiprocessing.Event()
            _stop_events[x] = multiprocessing.Event()
            # Get the IP's critical ports and add them to the scan list
            _ip_scanned_ports[_ips[x]] = _ports
            _critical_ports = self._client_data['_host_detail'][
                self._ips_to_hostname[_ips[x]]][
                self._ips_to_networks[_ips[x]]][
                'critical_ports']
            for port in _critical_ports:
                if port not in _ports:
                    _ip_scanned_ports[_ips[x]].append(port)
            _threads[x] = NetworkScanner(_ips[x], _ip_scanned_ports[_ips[x]],
                                         _queues[x], _start_events[x],
                                         _stop_events[x], self._conf)

        while True:
            # Get the current number of scanning threads
            _num_scanning = 0
            for event in _start_events:
                if event.is_set():
                    _num_scanning += 1

            if _num_scanning < _concurrent_scans:
                _need_to_scan = _concurrent_scans - _num_scanning
                for event in enumerate(_start_events):
                    if not event[1].is_set():
                        logging.debug('Informing thread to scan ip %s.' %
                                      _ips[event[0]])
                        _threads[event[0]].start()
                        event[1].set()
                        _need_to_scan -= 1
                    if _need_to_scan == 0:
                        break

            for event in enumerate(_stop_events):
                if event[1].is_set() and not _queues[event[0]].empty():
                    _thread_result = _queues[event[0]].get()
                    _index = event[0]
                    logging.debug('Received data: %s' % _thread_result)
                    if self.SCAN_SUCCESSFUL in str(_thread_result) \
                            or self.SCAN_FAILED in str(_thread_result):
                        self._receive_scan_data(_ips[_index],
                                                _queues[_index],
                                                _thread_result,
                                                _ip_scanned_ports[
                                                    _ips[_index]])
                        del _ips[_index]
                        del _queues[_index]
                        del _start_events[_index]
                        del _stop_events[_index]
                        del _threads[_index]
            if len(_queues) == 0:
                break

    def _receive_scan_data(self, ip, queue, result, scanned_ports):
        """Receive result data from scan.

        This will check the queue if result is successful and grab the result
        dict.

        :param ip: IP Address from _ips
        :param queue; Queue object from _queues
        :param result: _thread_result, successful scan or not
        :param scanned_ports: list of scanned ports
        """
        _scan_results = []
        _failed_critical_ports = []
        if self.SCAN_SUCCESSFUL in str(result) and not queue.empty():
            logging.debug('Received successful scan: Host(%s) Data(%s).' %
                          (ip, result))
            _scan_results = queue.get()
            _reason = 'reachable'
            logging.debug('Received results: Host(%s) Data(%s).' %
                          (ip, _scan_results))

            # Check our critical ports for the scanned ip
            _critical_ports = self._client_data['_host_detail'][
                self._ips_to_hostname[ip]][
                self._ips_to_networks[ip]]['critical_ports']
            if self.SCAN_FAILED not in str(result):
                for port in _critical_ports:
                    if port not in list(_scan_results):
                        _failed_critical_ports.append(port)
                        result = self.SCAN_FAILED
                        _reason = 'critical_ports'
        else:
            _reason = 'unreachable'
            logging.debug('Received failed scan: '
                          'Host(%s) Data(%s).' %
                          (ip, result))

        _result = {
            'results': {}
        }
        _result['results'][ip] = {
            'result': result,
            'reason': _reason,
            'open_ports': _scan_results,
            'host': self._ips_to_hostname[ip],
            'scanned_ports': scanned_ports,
            'failed_critical_ports': _failed_critical_ports
        }

        logging.debug('Final results: %s' % _result)
        self._client_data['_host_detail'][
            self._hostname][self._ips_to_networks[ip]].update(_result)
        self._result_data[self._hostname] = \
            self._client_data['_host_detail'][self._hostname]

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
        self._server = SocketListener((self._conf.bind_host,
                                       self._conf.bind_port), 'AF_INET')
        _recieved = False
        _client_data = None
        while True:
            # Bypass Listener and use SocketListener to set timeout
            self._server._socket.settimeout(self._conf.client.listener_timeout)
            try:
                connection = self._server.accept()
            except socket.timeout:
                # Send us back to run() to communicate the timeout.
                break
            while True:
                try:
                    _client_data = connection.recv()
                    logging.debug('Distributed data received from server: '
                                  '%s - Data: %s.' %
                                  (self._server._last_accepted[0],
                                   _client_data))
                    connection.send('validated')
                    _recieved = True
                except EOFError:
                    break
            connection.close()
            if _recieved:
                break
        self._server.close()
        self._server = None
        return _recieved, _client_data
