import os
from dotmap import DotMap


class Camera(object):
    ''' `sensed` sensor module for the Raspberry Pi NoIR camera. This
        module returns a JPEG image. '''

    def __init__(self, config: DotMap) -> None:
        if config.sensed.test is not True:
            import picamera
            self.camera = picamera.PiCamera()

    def get_data(self) -> dict:
        self.camera.capture('img.jpg')
        with open('img.jpg', 'rb') as fp:
            img = fp.read()
        os.remove('img.jpg')
        return {'camera': img}

    def test(self) -> dict:
        return {'camera': ''}


Sensor = Camera
