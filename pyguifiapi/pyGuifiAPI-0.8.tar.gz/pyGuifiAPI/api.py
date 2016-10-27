#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# guifiAPI.py - Guifi.net API client
# Copyright (C) 2012-2016 Pablo Castellano <pablo@anche.no>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


try:
    from urllib.request import Request, urlopen, URLError
    from urllib.parse import urlencode
except ImportError:
    # Python 2
    from urllib2 import Request, urlopen, URLError
    from urllib import urlencode
    # Warning: HTTPS requests do not do any verification of the server’s certificate.
    # Currently urllib2 does not support fetching of https locations through a proxy. This can be a problem.
    # http://www.voidspace.org.uk/python/articles/urllib2.shtml

from error import GuifiApiError
from constants import *

import json


class GuifiAPI(object):

    def __init__(self, username=None, passwd=None, host='test.guifi.net',
                 secure=True, retry_count=0, retry_delay=0, retry_errors=None,
                 authToken=None):

        self.setHost(host)
        self.secure = secure
        self.username = username
        self.passwd = passwd
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.retry_errors = retry_errors

        self.base_url = 'https://' if self.secure else 'http://'
        self.base_url += self.host

        self.base_api_url = self.base_url + '/api?'
        self.base_cnml_url = self.base_url + '/%s/guifi/cnml/%d/%s'
        self.base_gml_url = self.base_url + '/%s/guifi/gml/%d/%s'
        self.base_device_url = self.base_url + '/%s/guifi/device/%d/view'

        user_agent = 'pyGuifiAPI/0.7'
        self.headers = {'User-Agent': user_agent}

        if authToken:
            self.headers['Authorization'] = 'GuifiLogin auth=' + authToken
        self.authToken = authToken

    def getHost(self):
        return self.host

    def setUsername(self, username):
        if username != self.username:
            #invalidate auth token
            self.authToken = None
            self.username = username

    def setPassword(self, password):
        self.passwd = password

    def getAuthToken(self):
        return self.authToken

    def setAuthToken(self, authToken):
        self.authToken = authToken

    def setHost(self, host):
        """Checks for a valid host and set it as attribute"""
        if host.endswith('/'):
            host = host[:-1]

        self.host = host

    def sendRequest(self, data):
        """ Sends API request and returns json result"""
        url = self.base_api_url + data
        #print('<<<sendRequest>>> {} {}'.format(url, len(url)))
        #print('Headers: {}'.format(self.headers))

        req = Request(url, headers=self.headers)
        try:
            response = urlopen(req)
            #j = json.load(response)
            r = response.read()
            if isinstance(r, bytes):
                r = r.decode('utf8')
            j = json.loads(r)
            print(r)
        except URLError as e:
            #caza tambien HTTPError
            print(e.reason)
            raise
        except ValueError as e:
            print(e.reason)
            raise

        return self._parseResponse(j)

    def _parseResponse(self, jsondata):
        """ Parses json response.
            Returns a tuple with the code and the result of the request (it can be an errorenous response)
            Raises exception if any error code is unknown """
        print('<<<parseResponse>>>')
        codenum = jsondata.get('code')['code']
        codestr = jsondata.get('code')['str']

        print('Got code {num}: {msg}'.format(num=codenum, msg=codestr))

        if codenum == ANSWER_GOOD:
            responses = jsondata.get('responses')
            if isinstance(responses, list):
                if len(responses) == 1:
                    responses = responses[0]
                    print('Just one response')
                else:
                    print('There are several responses')
            return (codenum, responses)
        elif codenum == ANSWER_BAD:
            errors = jsondata.get('errors')
            if len(errors) == 1:
                errors = errors[0]
                print('Just one response (error)')
                print('Error {code}: {msg}'.format(code=errors['code'], msg=errors['str']))
                if 'extra' in errors:
                    print('Extra information: {msg}'.format(msg=errors['extra']))
            else:
                print('There are several responses (errors)')
                for e in errors:
                    print('Error {code}: {msg}'.format(code=e['code'], msg=e['str']))
                    if 'extra' in e:
                        print('Extra information: {msg}'.format(msg=e['extra']))
            return (codenum, errors)
        else:
            raise GuifiApiError('Unexpected return code: ' + codenum)

    def auth(self):
        """ Authenticate user and get the Authorization Token """

        if self.username is None or self.passwd is None:
            raise GuifiApiError('You need to set username and password first')

        self.authToken = None
        if 'Authorization' in self.headers:
            del self.headers['Authorization']

        # XXX: There's some kind of bug when you submit the Authorization header to this command
        # Then, you get 502 error if command is the last parameters specified
        # http://test.guifi.net/api?username=user1&password=pass1&command=guifi.auth.login
        # {"command":"","code":{"code":201,"str":"Request could not be completed, errors found"},"errors":[{"code":502,"str":"The given Auth token is invalid"}]}
        # Note 1: the command is not specified in the response (!!)
        # Note 2: it works well in firefox
        # A workaround fix is also using the method parameter which is added to the end in the dict structure
        #data = urlencode({'command':'guifi.auth.login', 'username':self.username, 'password':self.passwd})
        data = urlencode({'command': 'guifi.auth.login', 'username': self.username, 'password': self.passwd, 'method': 'password'})

        try:
            (codenum, response) = self.sendRequest(data)

            print('auth: {code}'.format(code=codenum))
            print(response)

            if codenum == ANSWER_GOOD:
                self.authToken = response.get('authToken')
                self.headers['Authorization'] = 'GuifiLogin auth=' + self.authToken
            else:
                # Expect just one error
                errorcode = response['code']
                if errorcode == CODE_ERROR_INVALID_TOKEN:  # Nosense (:?)
                    #{"errors":[{"code":403,"str":"Request is not valid: some input data is incorrect","extra":"Either the supplied username or password are not correct"}]}
                    raise GuifiApiError('Error during authentication: ' + str(errorcode) + ': ' + response['str'])
                else:
                    raise GuifiApiError('Unexpected return code: ' + str(errorcode))
        except URLError:  # Not connected to the Internets
            raise

    def addNode(self, title, zone_id, lat, lon, nick=None, body=None,
                zone_desc=None, notification=None, elevation=None,
                stable='Yes', graph_server=None, status='Planned'):

        if not self.is_authenticated():
            raise GuifiApiError('You have to be authenticated to run this action')

        data = {'command': 'guifi.node.add', 'title': title, 'zone_id': zone_id, 'lat': lat, 'lon': lon}

        if nick:
            data['nick'] = nick
        if body:
            data['body'] = body
        if zone_desc:
            data['zone_description'] = zone_desc
        if notification:
            data['notification'] = notification
        if elevation:
            data['elevation'] = elevation
        if stable != 'Yes':
            data['stable'] = 'No'
        if graph_server:
            data['graph_server'] = graph_server
        if status is not 'Planned':
            data['status'] = status

        params = urlencode(data)
        (codenum, response) = self.sendRequest(params)

        if codenum == ANSWER_GOOD:
            node_id = int(response.get('node_id'))
            print('Node {id} succesfully created'.format(id=node_id))
            print(self.urlForNode(node_id))
        else:
            # Everybody can create nodes
            extra = response.get('extra', None)
            raise GuifiApiError(response['str'], response['code'], extra)

        return node_id

    def urlForNode(self, nid):
        lang = 'es'
        return '%s/%s/node/%d' % (self.base_url, lang, nid)

    def urlForZone(self, zid):
        lang = 'es'
        return '%s/%s/node/%d' % (self.base_url, lang, zid)

    def urlForDevice(self, did):
        lang = 'es'
        return self.base_device_url % (lang, did)

    def updateNode(self, nid, title=None, nick=None, body=None, zone_id=None,
                   zone_description=None, notification=None, lat=None,
                   lon=None, elevation=None, stable=None, graph_server=None,
                   status=None):

        if not self.is_authenticated():
            raise GuifiApiError('You have to be authenticated to run this action')

        data = {'command': 'guifi.node.update', 'node_id': nid}
        if title:
            data['title'] = title
        if nick:
            data['nick'] = nick
        if body:
            data['body'] = body
        if zone_id:
            data['zone_id'] = zone_id
        if zone_description:
            data['zone_description'] = zone_description
        if notification:
            data['notification'] = notification
        if lat:
            data['lat'] = lat
        if lon:
            data['lon'] = lon
        if elevation:
            data['elevation'] = elevation
        if stable:
            data['stable'] = stable
        if status:
            data['status_flag'] = status

        params = urlencode(data)
        (codenum, response) = self.sendRequest(params)

        if codenum == ANSWER_GOOD:
            node_id = response['node']['node_id']
            print('Node {id} succesfully updated'.format(id=node_id))
            print('{base_url}/node/{id}'.format(base_url=self.base_url, id=node_id))
        else:
            # [{"code":500,"str":"Request could not be completed. The object was not found","extra":"zone_id =  is not a guifi node"}]}
            extra = response.get('extra', None)
            raise GuifiApiError(response['str'], response['code'], extra)

        return node_id

    def removeNode(self, nid):
        if not self.is_authenticated():
            raise GuifiApiError('You have to be authenticated to run this action')

        data = {'command': 'guifi.node.remove', 'node_id': nid}
        params = urlencode(data)
        (codenum, response) = self.sendRequest(params)

        if codenum == ANSWER_GOOD:
            print('Node {id} succesfully removed'.format(id=nid))
        else:
            # [{"code":500,"str":"Request could not be completed. The object was not found","extra":"node_id = 49836"}]}
            extra = response.get('extra', None)
            raise GuifiApiError(response['str'], response['code'], extra)

    def addZone(self, title, master, minx, miny, maxx, maxy, nick=None,
                mode='infrastructure', body=None, timezone='+01 2 2',
                graph_server=None, proxy_server=None, dns_servers=None,
                ntp_servers=None, ospf_zone=None, homepage=None,
                notification=None):

        if not self.is_authenticated():
            raise GuifiApiError('You have to be authenticated to run this action')

        data = {'command': 'guifi.zone.add', 'title': title, 'master': master,
                'minx': minx, 'miny': miny, 'maxx': maxx, 'maxy': maxy}

        if nick:
            data['nick'] = nick
        if mode != 'infrastructure':
            data['mode'] = mode
        if body:
            data['body'] = body
        if timezone != '+01 2 2':
            data['timezone'] = timezone
        if graph_server:
            data['graph_server'] = graph_server
        if proxy_server:
            data['proxy_server'] = proxy_server
        if dns_servers:
            data['dns_servers'] = dns_servers
        if ntp_servers:
            data['ntp_servers'] = ntp_servers
        if ospf_zone:
            data['ospf_zone'] = ospf_zone
        if homepage:
            data['homepage'] = homepage
        if notification:
            data['notification'] = notification

        params = urlencode(data)
        (codenum, response) = self.sendRequest(params)

        if codenum == ANSWER_GOOD:
            zone_id = int(response.get('zone_id'))
            print('Zone {id} succesfully created'.format(id=zone_id))
            print(self.urlForZone(zone_id))
        else:
            extra = response.get('extra', None)
            raise GuifiApiError(response['str'], response['code'], extra)

        return zone_id

    def updateZone(self, zid, title=None, nick=None, mode='infrastructure',
                   body=None, timezone='+01 2 2', graph_server=None,
                   proxy_server=None, dns_servers=None, ntp_servers=None,
                   ospf_zone=None, homepage=None, notification=None,
                   master=None, minx=None, miny=None, maxx=None, maxy=None):

        if not self.is_authenticated():
            raise GuifiApiError('You have to be authenticated to run this action')

        data = {'command': 'guifi.zone.update', 'zone_id': zid}
        params = urlencode(data)
        (codenum, response) = self.sendRequest(params)

        if codenum == ANSWER_GOOD:
            pass
        else:
            extra = response.get('extra', None)
            raise GuifiApiError(response['str'], response['code'], extra)

    def removeZone(self, zid):

        if not self.is_authenticated():
            raise GuifiApiError('You have to be authenticated to run this action')

        data = {'command': 'guifi.zone.remove', 'zone_id': zid}
        params = urlencode(data)
        (codenum, response) = self.sendRequest(params)

        if codenum == ANSWER_GOOD:
            pass
        else:
            extra = response.get('extra', None)
            raise GuifiApiError(response['str'], response['code'], extra)

    def addDevice(self, nid, rtype, mac, nick=None, notification=None,
                  comment=None, status=None, graph_server=None,
                  model_id=None, firmware=None, download=None, upload=None, mrtg_index=None):

        if not self.is_authenticated():
            raise GuifiApiError('You have to be authenticated to run this action')

        data = {'command': 'guifi.device.add', 'node_id': nid, 'type': rtype, 'mac': mac}

        if nick:
            data['nick'] = nick
        if notification:
            data['notification'] = notification
        if comment:
            data['comment'] = comment
        if status:
            data['status'] = status
        if graph_server:
            data['graph_server'] = graph_server

        if rtype == 'radio':
            if None in (model_id, firmware):
                raise ValueError("If rtype=='radio' you must specify model_id and firmware too")
            data['model_id'] = model_id
            data['firmware'] = firmware
        elif rtype == 'adsl':
            if None in (download, upload, mrtg_index):
                raise ValueError("If rtype=='adsl' you must specify download, upload and mrtg_index too")
            data['download'] = download
            data['upload'] = upload
            data['mrtg_index'] = mrtg_index
        elif rtype == 'generic':
            if mrtg_index is None:
                raise ValueError("If rtype=='generic' you must specify mrtg_index too")
            data['mrtg_index'] = mrtg_index

        params = urlencode(data)
        (codenum, response) = self.sendRequest(params)

        if codenum == ANSWER_GOOD:
            device_id = int(response.get('device_id'))
            print('Device {id} succesfully created'.format(id=device_id))
            print(self.urlForDevice(device_id))
        else:
            extra = response.get('extra', None)
            raise GuifiApiError(response['str'], response['code'], extra)

        return device_id

    def updateDevice(self, did, nid=None, nick=None, notification=None,
                     mac=None, comment=None, status=None, graph_server=None,
                     model_id=None, firmware=None, download=None, upload=None,
                     mrtg_index=None):

        if not self.is_authenticated():
            raise GuifiApiError('You have to be authenticated to run this action')

        data = {'command': 'guifi.device.update', 'device_id': did}

        # TODO: update nid. Is it safe to change it directly in the database?
        if nick:
            data['nick'] = nick
        if notification:
            data['notification'] = notification
        if mac:
            data['mac'] = mac
        if comment:
            data['comment'] = comment
        if status:
            data['flag'] = status
        if graph_server:
            data['graph_server'] = graph_server
        if model_id:
            data['model_id'] = model_id
        if firmware:
            data['firmware'] = firmware
        if download:
            data['download'] = download
        if upload:
            data['upload'] = upload
        if mrtg_index:
            data['mrtg_index'] = mrtg_index

        params = urlencode(data)
        (codenum, response) = self.sendRequest(params)

        if codenum == ANSWER_GOOD:
            print('Device {id} successfully updated'.format(id=did))
        else:
            extra = response.get('extra', None)
            raise GuifiApiError(response['str'], response['code'], extra)

    def removeDevice(self, did):

        if not self.is_authenticated():
            raise GuifiApiError('You have to be authenticated to run this action')

        data = {'command': 'guifi.device.remove', 'device_id': did}
        params = urlencode(data)
        (codenum, response) = self.sendRequest(params)

        if codenum == ANSWER_GOOD:
            print('Device {id} successfully removed'.format(id=did))
        else:
            extra = response.get('extra', None)
            raise GuifiApiError(response['str'], response['code'], extra)

    def addRadio(self, mode, did, mac, angle=None, gain=None, azimuth=None,
                 amode=None, ssid=None, protocol=None, channel=None, clients='Yes'):

        if not self.is_authenticated():
            raise GuifiApiError('You have to be authenticated to run this action')

        data = {'command': 'guifi.radio.add', 'mode': mode, 'device_id': did, 'mac': mac}

        if angle:
            data['antenna_angle'] = angle
        if gain:
            data['antenna_gain'] = gain
        if azimuth:
            data['antenna_azimuth'] = azimuth
        if amode:
            data['antenna_mode'] = amode

        if mode == 'ap':
            if None in (ssid, protocol, channel, clients):
                raise ValueError("If mode=='ap' you must specify ssid, protocol, channel and clients too")
            data['ssid'] = ssid
            data['protocol'] = protocol
            data['channel'] = channel
            data['clients_accepted'] = clients
        elif mode == 'ad-hoc':
            if None in (ssid, protocol, channel):
                raise ValueError("If mode=='ad-hoc' you must specify ssid, protocol, and channel too")
            data['ssid'] = ssid
            data['protocol'] = protocol
            data['channel'] = channel
        else:
            print(mode)
            raise NotImplementedError

        params = urlencode(data)
        (codenum, response) = self.sendRequest(params)

        if codenum == ANSWER_GOOD:
            # TODO: qué devolver? array tb?
            radiodev_counter = int(response.get('radiodev_counter'))
            interfaces = response.get('interfaces')
            print('Radio {counter} successfully created'.format(counter=radiodev_counter))
            print(self.urlForDevice(int(did)))
        else:
            extra = response.get('extra', None)
            raise GuifiApiError(response['str'], response['code'], extra)

        return (radiodev_counter, interfaces)

    def updateRadio(self, did, radiodev, angle=None, gain=None,
                    azimuth=None, amode=None):

        if not self.is_authenticated():
            raise GuifiApiError('You have to be authenticated to run this action')

        data = {'command': 'guifi.radio.update', 'device_id': did, 'radiodev_counter': radiodev}
        params = urlencode(data)
        (codenum, response) = self.sendRequest(params)

        if codenum == ANSWER_GOOD:
            print('Radio {id}/{radiodev} successfully updated'.format(id=did, radiodev=radiodev))
        else:
            extra = response.get('extra', None)
            raise GuifiApiError(response['str'], response['code'], extra)

    def removeRadio(self, did, radiodev):

        if not self.is_authenticated():
            raise GuifiApiError('You have to be authenticated to run this action')

        data = {'command': 'guifi.radio.remove', 'device_id': did, 'radiodev_counter': radiodev}
        params = urlencode(data)
        (codenum, response) = self.sendRequest(params)

        if codenum == ANSWER_GOOD:
            print('Radio {radio} from device {id} successfully removed'.format(radio=radiodev, id=did))
        else:
            extra = response.get('extra', None)
            raise GuifiApiError(response['str'], response['code'], extra)

    def addInterface(self, did, radiodev):

        if not self.is_authenticated():
            raise GuifiApiError('You have to be authenticated to run this action')

        data = {'command': 'guifi.interface.add', 'device_id': did, 'radiodev_counter': radiodev}
        params = urlencode(data)
        (codenum, response) = self.sendRequest(params)

        # "responses":{"ipv4":[{"ipv4_type":"1","ipv4":"10.64.3.33","netmask":"255.255.255.224"}],"interface_id":76140}
        if codenum == ANSWER_GOOD:
            iid = int(response.get('interface_id'))
            ipv4 = response.get('ipv4')
            print('Interface {id} succesfully created'.format(id=iid))
            print(self.urlForDevice(int(did)))
        else:
            extra = response.get('extra', None)
            raise GuifiApiError(response['str'], response['code'], extra)

        return (iid, ipv4)

    def removeInterface(self, iid):

        if not self.is_authenticated():
            raise GuifiApiError('You have to be authenticated to run this action')

        data = {'command': 'guifi.interface.remove', 'interface_id': iid}
        params = urlencode(data)
        (codenum, response) = self.sendRequest(params)

        if codenum == ANSWER_GOOD:
            print('Interface {id} succesfully removed'.format(id=iid))
        else:
            extra = response.get('extra', None)
            raise GuifiApiError(response['str'], response['code'], extra)

    def addLink(self, fromdid, fromradiodev, todid, toradiodev,
                ipv4=None, status='Working'):

        if not self.is_authenticated():
            raise GuifiApiError('You have to be authenticated to run this action')

        data = {'command': 'guifi.link.add', 'from_device_id': fromdid,
                'from_radiodev_counter': fromradiodev, 'to_device_id': todid,
                'to_radiodev_counter': toradiodev}
        params = urlencode(data)
        (codenum, response) = self.sendRequest(params)

        if codenum == ANSWER_GOOD:
            lid = int(response.get('link_id'))
            ipv4 = response.get('ipv4')
            print('Link {id} successfully created'.format(id=lid))
            print(self.urlForDevice(int(fromdid)))
        else:
            # FIXME: Crashes when there are several errors and extra is a list (no has_key())
            extra = response.get('extra', None)
            raise GuifiApiError(response['str'], response['code'], extra)

        return (lid, ipv4)

    def updateLink(self, lid, ipv4=None, status=None, routing=None):

        if not self.is_authenticated():
            raise GuifiApiError('You have to be authenticated to run this action')

        data = {'command': 'guifi.link.update', 'link_id': lid}

        if ipv4:
            data['ipv4'] = ipv4
        if status:
            data['status'] = status
        if routing:
            data['routing'] = routing

        params = urlencode(data)
        (codenum, response) = self.sendRequest(params)

        if codenum == ANSWER_GOOD:
            print('Link {id} succesfully updated'.format(id=lid))
        else:
            extra = response.get('extra', None)
            raise GuifiApiError(response['str'], response['code'], extra)

    def removeLink(self, lid):

        if not self.is_authenticated():
            raise GuifiApiError('You have to be authenticated to run this action')

        data = {'command': 'guifi.link.remove', 'link_id': lid}
        params = urlencode(data)
        (codenum, response) = self.sendRequest(params)

        if codenum == ANSWER_GOOD:
            print('Link {id} succesfully removed'.format(id=lid))
        else:
            extra = response.get('extra', None)
            raise GuifiApiError(response['str'], response['code'], extra)

    def getModels(self, type=None, fid=None, supported=None):
        data = {'command': 'guifi.misc.model'}
        if type:
            data['type'] = type
        if fid:
            data['fid'] = fid
        if supported:
            data['supported'] = supported

        params = urlencode(data)
        (codenum, response) = self.sendRequest(params)

        if codenum == ANSWER_GOOD:
            return response['models']
        else:
            raise GuifiApiError(response['str'], response['code'], response['extra'])

    def getManufacturers(self):
        data = {'command': 'guifi.misc.manufacturer'}
        params = urlencode(data)
        (codenum, response) = self.sendRequest(params)

        if codenum == ANSWER_GOOD:
            return response['manufacturers']
        else:
            extra = response.get('extra', None)
            raise GuifiApiError(response['str'], response['code'], extra)

    def getFirmwares(self, model_id=None):
        data = {'command': 'guifi.misc.firmware', 'model_id': model_id}
        params = urlencode(data)
        (codenum, response) = self.sendRequest(params)

        if codenum == ANSWER_GOOD:
            return response['firmwares']
        else:
            extra = response.get('extra', None)
            raise GuifiApiError(response['str'], response['code'], extra)

    def getProtocols(self):
        data = {'command': 'guifi.misc.protocol'}
        params = urlencode(data)
        (codenum, response) = self.sendRequest(params)

        if codenum == ANSWER_GOOD:
            return response['protocols']
        else:
            extra = response.get('extra', None)
            raise GuifiApiError(response['str'], response['code'], extra)

    def getChannels(self, protocol):
        data = {'command': 'guifi.misc.channel', 'protocol': protocol}
        params = urlencode(data)
        (codenum, response) = self.sendRequest(params)

        if codenum == ANSWER_GOOD:
            return response['channels']
        else:
            extra = response.get('extra', None)
            raise GuifiApiError(response['str'], response['code'], extra)

    def is_authenticated(self):
        return self.authToken is not None

    #http://test.guifi.net/es/guifi/cnml/3671/zones
    #returns file descriptor to be read
    # It may take some seconds depending on the server load...
    def downloadCNML(self, zid, ctype='nodes'):
        if ctype not in ['zones', 'nodes', 'detail']:
            raise ValueError

        lang = 'es'
        url = self.base_cnml_url % (lang, zid, ctype)
        print('Downloading CNML: {url}'.format(url=url))

        req = Request(url, headers=self.headers)
        response = urlopen(req)
        return response

    # http://guifi.net/es/guifi/gml/21629/links
    def downloadGML(self, zid, ctype='nodes'):
        if ctype not in ['nodes', 'links']:
            raise ValueError

        lang = 'es'
        url = self.base_gml_url % (lang, zid, ctype)
        print('Downloading GML: {url}'.format(url=url))

        req = Request(url, headers=self.headers)
        response = urlopen(req)
        return response

"""
guifi.zone.nearest
guifi.radio.nearest
"""
