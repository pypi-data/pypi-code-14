from __future__ import unicode_literals
import hueobject
import sensor


class HueDevice(hueobject.HueLLDevice):
    @staticmethod
    def factory(devices):
        # If devices only holds a single sensor, use it
        if len(devices) == 1:
            return devices[0]
        presence_sensor = False
        temp_sensor = False
        light_sensor = False
        for d in devices:
            if isinstance(d, sensor.PresenceSensor):
                presence_sensor = True
            elif isinstance(d, sensor.TemperatureSensor):
                temp_sensor = True
            elif isinstance(d, sensor.LightLevelSensor):
                light_sensor = True
        if presence_sensor and temp_sensor and light_sensor:
            return HueMotionDetectorDevice(devices)
        raise RuntimeError('Unsupported device')


class HueMultiSensorDevice(HueDevice):
    def __init__(self, sensors):
        self.sensors = sensors

    def _get_sensor_by_type(self, sensor_type):
        for s in self.sensors:
            if isinstance(s, sensor_type):
                return s

    @property
    def mac_address(self):
        return self.sensors[0].mac_address


class HueMotionDetectorDevice(HueMultiSensorDevice):
    @property
    def presence_sensor(self):
        return self._get_sensor_by_type(sensor.PresenceSensor)

    @property
    def temperature_sensor(self):
        return self._get_sensor_by_type(sensor.TemperatureSensor)

    @property
    def light_level_sensor(self):
        return self._get_sensor_by_type(sensor.LightLevelSensor)

    @property
    def name(self):
        return self.presence_sensor.name

    @property
    def temperature(self):
        return self.temperature_sensor.temperature

    @property
    def light_level(self):
        return self.light_level_sensor.light_level

    @property
    def presence(self):
        return self.presence_sensor.presence

    @property
    def battery(self):
        return self.sensors[0].battery

    @property
    def hue_id(self):
        return self.sensors[0].hue_id

