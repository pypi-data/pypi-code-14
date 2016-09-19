import exception as excep
import os
from colorama import init
init()

class Colors:
	PASS = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	NAME = '\033[96m'
	ENDC = '\033[0m'

class Smileys:
	HAPPY = ":)"
	SAD = ":("
	CONFUSED = ":S"
	
def display(testResult):
	if testResult == None:
		return

	color, smiley = _selectColorAndSmiley(testResult)
	print "{}{} {}{}".format(color, smiley, testResult.description, Colors.ENDC)
	if testResult.message:
		 print "  - {}".format(testResult.message)

def displayTestName(testName):
	print "{}Testing: {}{}".format(Colors.NAME, testName, Colors.ENDC)

def displayUpdate(fileName):
	print "{}Updated: {}{}".format(Colors.WARNING, os.path.basename(fileName), Colors.ENDC)

def displayCustom(message):
	print message

def _selectColorAndSmiley(testResult):
	if testResult.hasPassed:
		return Colors.PASS, Smileys.HAPPY
	if type(testResult.message) is excep.SourceException:
		return Colors.WARNING, Smileys.CONFUSED
	return Colors.FAIL, Smileys.SAD

def displayError(message):
	print "{}{} {}{}".format(Colors.WARNING, Smileys.CONFUSED, message, Colors.ENDC)