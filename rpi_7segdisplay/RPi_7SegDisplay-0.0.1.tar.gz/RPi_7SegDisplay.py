import RPi.GPIO as GPIO
import multiprocessing
import signal
import sys
from time import sleep

_CHARACTERS = {
    '0': 0b11000000,
    '1': 0b11111001,
    '2': 0b10100100,
    '3': 0b10110000,
    '4': 0b10011001,
    '5': 0b10010010,
    '6': 0b10000010,
    '7': 0b11111000,
    '8': 0b10000000,
    '9': 0b10010000,
    ' ': 0b11111111,
    '-': 0b10111111,
    '.': 0b01111111
    }

_BLANK = [_CHARACTERS[' ']] * 8


def init(data_pin, clock_pin, latch_pin):
    global _data, _clock, _latch, _proc
    _data = data_pin
    _clock = clock_pin
    _latch = latch_pin

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup([data_pin, clock_pin, latch_pin], GPIO.OUT)

    if (len(multiprocessing.active_children()) == 0):
        _proc = multiprocessing.Process(target=_display)
        _proc.start()


def _shift(byte):
    for i in range(7, -1, -1):
        GPIO.output(_data, byte & (1 << i))
        GPIO.output(_clock, 1)
        GPIO.output(_clock, 0)


def _write(message):
    for i, char in enumerate(message):
        _shift(2 << i)
        _shift(char)
        GPIO.output(_latch, 1)
        GPIO.output(_latch, 0)
        sleep(0.002)


def _display():
    while True:
        if not _queue.empty():
            text = _queue.get()
        _write(text)


def show(message):
    result = []
    if not _queue.full():
        for i, char in enumerate(message):
            if (char == '.' and i > 0):
                result[-1] -= 128
            elif (char != '.'):
                result.append(_CHARACTERS[char])
        _queue.put(result)


def stop():
    _proc.terminate()
    _write(_BLANK)
    GPIO.cleanup()

def _signal_handler(signal, frame):
    stop()
    sys.exit(0)

_queue = multiprocessing.Queue(2)
_queue.put(_BLANK)
signal.signal(signal.SIGINT, _signal_handler)
