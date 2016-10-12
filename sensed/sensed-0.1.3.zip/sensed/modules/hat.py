from dotmap import DotMap


class Hat(object):
    ''' `sensed` sensor module for the Raspberry Pi Sense HAT. This
        module returns a dictionary of all built in sensors. '''

    def __init__(self, config: DotMap) -> None:
        if config.sensed.test is not True:
            from sense_hat import SenseHat
            self.sense = SenseHat()

    def get_data(self) -> dict:
        # Environmental sensors
        humid = self.sense.humidity
        temp = self.sense.temperature
        temp_h = self.sense.get_temperature_from_humidity()
        temp_p = self.sense.get_temperature_from_pressure()
        press = self.sense.pressure

        # IMU (inertial measurement unit) sensors
        orient_r = self.sense.orientation_radians
        orient_d = self.sense.orientation
        compass = self.sense.compass
        compass_r = self.sense.compass_raw
        gyro = self.sense.gyroscope
        gyro_r = self.sense.gyroscope_raw
        accel = self.sense.accelerometer
        accel_r = self.sense.accelerometer_raw

        return {'environment': {'humidity': humid,
                                'temperature': temp,
                                'temperature_h': temp_h,
                                'temperature_p': temp_p,
                                'pressure': press},
                'imu': {'orientation_rad': orient_r,
                        'orientation_deg': orient_d,
                        'compass': compass,
                        'compass_r': compass_r,
                        'gyroscope': gyro,
                        'gyroscope_r': gyro_r,
                        'accelerometer': accel,
                        'accelerometer_raw': accel_r}}

    def test(self) -> dict:
        return {'environment': {'humidity': 1,
                                'temperature': 2,
                                'temperature_h': 3,
                                'temperature_p': 4,
                                'pressure': 5},
                'imu': {'orientation_rad': 6,
                        'orientation_deg': 7,
                        'compass': 8,
                        'compass_r': 9,
                        'gyroscope': 10,
                        'gyroscope_r': 11,
                        'accelerometer': 12,
                        'accelerometer_raw': 13}}


Sensor = Hat
