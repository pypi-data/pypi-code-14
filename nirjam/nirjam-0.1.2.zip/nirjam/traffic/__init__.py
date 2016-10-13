from nirjam.traffic import network
import RPi.GPIO as GPIO

traficlightip = "192.168.1.1"
red = 26
amber = 24
green = 22


def ipaddress(ip):
    global traficlightip
    traficlightip = ip
    network.call(traficlightip)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(red, GPIO.OUT)
    GPIO.setup(amber, GPIO.OUT)
    GPIO.setup(green, GPIO.OUT)


def pindefine(redpin, amberpin, greenpin):
    global red
    global amber
    global green
    red = redpin
    amber = amberpin
    green = greenpin


def GreenOn():
    network.say("GreenOn")
    GPIO.output(green, True)


def GreenOff():
    network.say("GreenOff")
    GPIO.output(green, False)


def AmberOn():
    network.say("AmberOn")
    GPIO.output(amber, True)


def AmberOff():
    network.say("AmberOff")
    GPIO.output(amber, False)


def RedOn():
    network.say("RedOn")
    GPIO.output(red, True)


def RedOff():
    network.say("RedOff")
    GPIO.output(red, False)


def AllOn():
    network.say("AllOn")
    GPIO.output(red, True)
    GPIO.output(amber, True)
    GPIO.output(green, True)

def AllOff():
    network.say("AllOff")
    GPIO.output(red, False)
    GPIO.output(amber, False)
    GPIO.output(green, False)


def cleanup():
    network.say("AllOff")
    GPIO.output(red, False)
    GPIO.output(amber, False)
    GPIO.output(green, False)
    global red
    global amber
    global green
    red = 26
    amber = 24
    green = 22
    global traficlightip
    traficlightip = "192.168.1.1"
