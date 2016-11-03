try:
    from RPi import GPIO
except:
    print "EMULATING GPIO!"
    from .emulate import GPIO

GPIO.setmode(GPIO.BOARD)

class LightSensor(object):

    def __init__(self, pin):
        self._pin = pin
        GPIO.setup(pin, GPIO.IN)
        self._callback = None

    def read(self):
        return GPIO.input(self._pin)

    def one_shot_lighting_change(self, callback):
        if self._callback:
            GPIO.remove_event_detect(self._pin)
        self._callback = callback
        GPIO.add_event_detect(self._pin, GPIO.BOTH, callback=self._one_shot_callback)

    def _one_shot_callback(self, pin):
        if self._callback is None:
            return
        input = 0
        for i in range(100):
            input += self.read()
        if input > 75: # 75% confidence there is light
            self._callback(True)
            self._callback = None
        if input < 25: # 75% confidence it is dark
            self._callback(False)