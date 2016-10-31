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
import threading
import socket


class NetworkScanner(threading.Thread):
    """Client NetworkScanner thread for net-survey."""

    SCAN_SUCCESSFUL = 'success'
    SCAN_FAILED = 'failed'
    START_SCAN = 'start_scan'
    HOLD_SCAN = 'hold_scan'

    def __init__(self, server_ip, ports, queue, start_event, stop_event, conf):
        self._server_ip = server_ip
        self._ports = ports
        self._queue = queue
        self._start_event = start_event
        self._stop_event = stop_event
        self._conf = conf
        self._open_ports = []
        threading.Thread.__init__(self)

    def run(self):
        """Main run process for NetworkScanner."""

        _scan_result = self.SCAN_FAILED

        # Wait for start event
        self._start_event.wait()
        _scan_result, self._open_ports = \
            self.scan_host(self._server_ip, self._ports)

        # Notify stop event, status of scan, and data
        self._stop_event.set()
        self._queue.put(_scan_result)
        if _scan_result == self.SCAN_SUCCESSFUL:
            self._queue.put(self._open_ports)

    def scan_host(self, ip, ports):
        """Scan host thread.

        This method performs work on the neighboring ip and scans the ports
        passed to the class instance.

        :param ip: a valid ip address
        :param ports: a list of ports to scan
        """
        _success = self.SCAN_SUCCESSFUL
        _results = []

        for port in ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                logging.debug('Scanning host: %s:%s' % (self._server_ip, port))
                result = s.connect_ex((ip, port))
                if result == 0:
                    _results.append(port)
                s.close()
            except socket.gaierror:
                logging.error('Hostname could not be resolved: %s' %
                              ip)
                _success = self.SCAN_FAILED
                break
            except socket.error:
                logging.error('Cloud not connect to host: %s.' %
                              ip)
                _success = self.SCAN_FAILED
                break

        return _success, _results
