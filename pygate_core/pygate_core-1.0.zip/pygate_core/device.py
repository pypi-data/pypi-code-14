#allows a device to manage it's cloud presence.

from pygate_core import cloud


class Device(object):
    '''allows a device to manage it's cloud presence'''

    def __init__(self, moduleName, deviceId):
        result = super(Device, self).__init__()
        self._deviceId = deviceId
        self._moduleName = moduleName
        return result

    def addAsset(self, id, name, description, assetType, profile, style = "Undefined"):
        """add asset"""
        cloud.addAsset(self._moduleName, self._deviceId, id, name, description, assetType, profile, style)

    def deleteAsset(self, id):
        cloud.deleteAsset(self._moduleName, self._deviceId, id)

    def createDevice(self, name, description):
        """add device"""
        cloud.addDevice(self._moduleName, self._deviceId, name, description)

    def send(self, value, actuator):
        cloud.send(self._moduleName, self._deviceId, actuator, value)

    def getValue(self, asset):
        """
        get the current value for the specified asset.
        :param asset: name of asset
        :return:
        """
        return cloud.getAssetState(self._moduleName, self._deviceId, asset)