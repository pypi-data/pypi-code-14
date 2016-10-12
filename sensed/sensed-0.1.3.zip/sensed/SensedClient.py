import struct
import socket
import msgpack

from dotmap import DotMap
from typing import List
from sensed import Headers
from sensed.Types import Host, HostList, MetaData, SensorData, SensorList


class SensedClient(object):

    __version__ = '0.1.1'
    __author__ = 'R. Cody Maden'

    def __init__(self, config: DotMap) -> None:
        self.hosts = config.senselog.hosts
        for h in range(len(self.hosts)):
            self.hosts[h] = tuple([self.hosts[h][0], int(self.hosts[h][1])])
        self.interval = config.senselog.interval

    def get_all_meta(self, hosts: HostList=None) -> List[MetaData]:
        if not hosts:
            hosts = self.hosts
        metas = []
        for host in hosts:
            meta = self.get_meta(host)
            metas.append(meta)
        return metas

    def get_all_sensors(self, hosts: HostList=None) -> List[SensorData]:
        if not hosts:
            hosts = self.hosts
        datas = []
        for host in hosts:
            data = self.get_sensors(host)
            datas.append(data)
        return datas

    def get_meta(self, host: Host) -> MetaData:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(Headers.ID, host)

        raw_data = s.recv(1024)
        raw_meta = raw_data[2:]
        meta = msgpack.unpackb(raw_meta)

        return meta

    def get_sensors(self, host: Host, sensors: SensorList=[]) -> SensorData:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        req = msgpack.packb(sensors)
        s.sendto(Headers.REQ + req, host)

        raw_size = s.recv(4)
        size = struct.unpack('I', raw_size)[0]

        raw_data = s.recv(size)
        header = raw_data[:2]
        data = msgpack.unpackb(raw_data[2:])
        data['header'] = header

        return data
