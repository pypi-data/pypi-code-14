class GPIO(object):

    BOARD = 0

    IN = 0
    BOTH = 1

    count = 0

    @staticmethod
    def setup(*args):
        pass

    @staticmethod
    def setmode(*args):
        pass

    @staticmethod
    def input(pin):
        GPIO.count += 1
        if GPIO.count < 600 or GPIO.count > 5000:
            return 0
        else:
            return 1

    @staticmethod
    def add_event_detect(pin, which, callback):
        GPIO.count += 1
        import time, threading
        class T(threading.Thread):

            def run(self):
                while True:
                    time.sleep(2.0)
                    callback(pin)
        GPIO.t = T()
        GPIO.t.start()
