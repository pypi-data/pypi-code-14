from __future__ import unicode_literals
import hueobject


class Config(hueobject.HueObject):
    # Versions
    @property
    def api_version(self):
        return self._json['apiversion']

    @property
    def version(self):
        return self._json['swversion']

    @property
    def bridge_id(self):
        return self._json['bridgeid']

    # Network stuff
    @property
    def dhcp(self):
        return self._json['dhcp']

    @property
    def gateway(self):
        return self._json['gateway']

    @property
    def mac(self):
        return self._json['mac']

    @property
    def netmask(self):
        return self._json['netmask']

    @property
    def zigbeechannel(self):
        return self._json['zigbeechannel']

    @property
    def factorynew(self):
        return self._json['factorynew']

    @property
    def timezone(self):
        return self._json['timezone']

