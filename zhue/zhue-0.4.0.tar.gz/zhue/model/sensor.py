from __future__ import unicode_literals
import hueobject
import re


def factory(bridge, hue_id, json):
    if json['type'] == 'ZLLTemperature':
        return TemperatureSensor(bridge, hue_id, json)
    elif json['type'] == 'ZLLLightLevel':
        return LightLevelSensor(bridge, hue_id, json)
    elif json['type'] == 'ZLLPresence':
        return PresenceSensor(bridge, hue_id, json)
    elif json['type'] == 'ZLLSwitch':
        return SwitchSensor(bridge, hue_id, json)
    else:
        return Sensor(bridge, hue_id, json)


class Sensor(hueobject.HueLLDevice):
    def __init__(self, *args, **kwargs):
        super(Sensor, self).__init__('sensors', *args, **kwargs)

    @property
    def config(self):
        return SensorConfig(self._json['config'])

    @property
    def state(self):
        return SensorState(self._json['state'])

    @property
    def battery(self):
        return self.config.battery

    @property
    def has_battery(self):
        return self.battery is not None


class SensorConfig(hueobject.HueObject):
    @property
    def battery(self):
        return self._json.get('battery', None)


class SensorState(hueobject.HueObject):
    @property
    def last_updated(self):
        return self._json['lastupdated']


class LightLevelSensor(Sensor):
    @property
    def config(self):
        return LightLevelSensorConfig(self._json['config'])

    @property
    def state(self):
        return LightLevelSensorState(self._json['state'])

    @property
    def light_level(self):
        return self.state.light_level


class LightLevelSensorConfig(SensorConfig):
    @property
    def alert(self):
        return self._json['alert']

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


class LightLevelSensorState(SensorState):
    @property
    def light_level(self):
        return self._json['lightlevel']

    @property
    def dark(self):
        return self._json['dark']

    @property
    def daylight(self):
        return self._json['daylight']


class TemperatureSensor(Sensor):
    @property
    def config(self):
        return TemperatureSensorConfig(self._json['config'])

    @property
    def state(self):
        return TemperatureSensorState(self._json['state'])

    @property
    def temperature(self):
        return self.state.temperature


class TemperatureSensorConfig(LightLevelSensorConfig):
    pass


class TemperatureSensorState(SensorState):
    @property
    def temperature(self):
        return float(self._json['temperature'] / 100.0)


class PresenceSensor(Sensor):
    @property
    def config(self):
        return PresenceSensorConfig(self._json['config'])

    @property
    def state(self):
        return PresenceSensorState(self._json['state'])

    @property
    def presence(self):
        return self.state.presence

    @property
    def battery(self):
        return self.config.battery


class PresenceSensorConfig(SensorConfig):
    pass


class PresenceSensorState(SensorState):
    @property
    def presence(self):
        return self._json['presence']


class SwitchSensor(Sensor):
    @property
    def config(self):
        return SwitchSensorConfig(self._json['config'])


class SwitchSensorConfig(SensorConfig):
    @property
    def on(self):
        return self._json['on']

    @property
    def reachable(self):
        return self._json['reachable']

    @property
    def pending(self):
        return self._json['pending']

