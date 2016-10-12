import time
import struct
import msgpack
import threading
import socketserver

from dotmap import DotMap
from typing import Tuple, Any
from sensed.Types import Host, SensorList
from sensed import Headers


class SensedServer(socketserver.BaseRequestHandler):

    __version__ = '0.1.4'
    __author__ = 'R. Cody Maden'

    def handle(self):
        data, host = self.mp_recv()
        packet = {}
        if data.header == Headers.ID:
            # Metadata request recieved
            sensors = list(self.server.sensors.keys())
            packet = {'name': self.server.config.sensed.name,
                      'sensors': sensors}
            header = Headers.ID
        elif data.header == Headers.REQ:
            # Sensor data request recieved
            if not data['body']:
                data['body'] = []  # Discard erroneous data (TODO: send error)
            packet = self.get_sensors(data['body'])
            header = Headers.REQ
        else:
            # Erroneous packet header supplied
            packet = {'_error': 'Invalid header'}
            header = Headers.ERR

        packet['timestamp'] = int(time.time())
        self.mp_send(header, packet, host)

    def get_sensors(self, sensors: SensorList=[]) -> dict:
        '''
        Using the configured list of sensors, queries them
        for data. If `sensors` is supplied, only the listed
        sensors will be queried.
        '''
        sensors = [s.decode('ascii') for s in sensors]
        ret = {'sensors': {}}
        for sensor in self.server.sensors:
            if len(sensors) == 0 or sensor in sensors:
                if self.server.config.sensed.test is True:
                    data = self.server.sensors[sensor].test()
                else:
                    data = self.server.sensors[sensor].get_data()
                ret['sensors'][sensor] = data
        return ret

    def mp_send(self, header: str, data: dict, host: Host):
        '''
        Sends data over the UDP socket in MessagePack format.
        First sends a four byte packet representing the size of the
        data to follow.
        '''
        mdata = header + msgpack.packb(data)
        if header == Headers.REQ:
            size = struct.pack('I', len(mdata))
            self.request[1].sendto(size, host)
        self.request[1].sendto(mdata, host)

    def mp_recv(self) -> Tuple[DotMap, Any]:
        packet = self.request[0]
        host = self.client_address
        header = packet[:2]
        data = packet[2:]
        if len(data) > 0:
            data = {'header': header,
                    'body': msgpack.unpackb(data)}
        else:
            data = {'header': header, 'body': []}

        return DotMap(data), host

    def create_event_thread(self, func, *args) -> None:
        '''
        Used by modules to start an event loop from a method
        defined within the module.
        '''
        def loop():
            while True:
                func(*args)

        t = threading.Thread(target=loop)
        t.daemon = True
        t.start()
