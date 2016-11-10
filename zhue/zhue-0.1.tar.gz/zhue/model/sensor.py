from __future__ import unicode_literals
import hueobject


def factory(bridge, hue_id, json):
    if json['type'] == 'ZLLTemperature':
        return TemperatureSensor(bridge, hue_id, json)
    elif json['type'] == 'ZLLLightLevel':
        return LightLevelSensor(bridge, hue_id, json)
    elif json['type'] == 'ZLLSwitch':
        return SwitchSensor(bridge, hue_id, json)
    else:
        return Sensor(bridge, hue_id, json)


class Sensor(hueobject.HueDevice):
    def __init__(self, *args, **kwargs):
        super(Sensor, self).__init__('sensors', *args, **kwargs)

    @property
    def config(self):
        return self._json['config']


class SensorConfig(hueobject.HueObject):
    pass


class LightLevelSensor(Sensor):
    @property
    def config(self):
        return LightLevelSensorConfig(self._json['config'])


class LightLevelSensorConfig(SensorConfig):
    @property
    def alert(self):
        return self._json['alert']

    @property
    def battery(self):
        return self._json['battery']

    @property
    def ledindication(self):
        return self._json['ledindication']

    @property
    def pending(self):
        return self._json['pending']

    @property
    def on(self):
        return self._json['on']

    @property
    def reachable(self):
        return self._json['reachable']

    @property
    def usertest(self):
        return self._json['usertest']


class TemperatureSensor(Sensor):
    @property
    def config(self):
        return TemperatureSensorConfig(self._json['config'])

    @property
    def state(self):
        return TemperatureSensorState(self._json['state'])


class TemperatureSensorConfig(LightLevelSensorConfig):
    pass


class TemperatureSensorState(hueobject.HueObject):
    @property
    def temperature(self):
        return float(self._json['temperature'] / 100.0)

    @property
    def lastupdated(self):
        return self._json['lastupdated']


class SwitchSensor(Sensor):
    @property
    def config(self):
        return SwitchSensorConfig(self._json['config'])


class SwitchSensorConfig(SensorConfig):
    @property
    def battery(self):
        return self._json['battery']

    @property
    def on(self):
        return self._json['on']

    @property
    def reachable(self):
        return self._json['reachable']

    @property
    def pending(self):
        return self._json['pending']

