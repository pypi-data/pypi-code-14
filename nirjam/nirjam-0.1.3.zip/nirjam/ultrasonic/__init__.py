import RPi.GPIO as GPIO
import time

GPIO_TRIGGER = 16
GPIO_ECHO = 18
elapsed = 0
distance = 0
stop = 0
start = 0
finaldistance = 0


def setpin(trigger, echo):
    # Sets pin
    global GPIO_TRIGGER
    global GPIO_ECHO
    GPIO_TRIGGER = trigger
    GPIO_ECHO = echo
    # Sets pin in RPi.GPIO and sets pin to be input or output
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    GPIO.output(GPIO_TRIGGER, False)


def sense():
    global stop
    global start
    global elapsed
    global distance
    global finaldistance
    # Measures time taken for bounce back
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()
    while GPIO.input(GPIO_ECHO) == 0:
        start = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        stop = time.time()
    # Calculates time taken
    elapsed = stop - start
    # Calculated distance in meters
    distance = elapsed * 34000
    # Halves distance to calculate object's distance
    finaldistance = distance / 2
    return finaldistance

