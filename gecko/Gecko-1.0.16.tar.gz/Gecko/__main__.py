﻿import sys
import logging
import argparse
import inspect

import apscheduler
from apscheduler.schedulers.background import BackgroundScheduler

from Gecko import Gecko 
import GeckoIO

import importlib
import os

import string

from simulator import simulate

# Get templates for generating application files
import pkg_resources
resource_package = 'Gecko' 

resource_path = os.path.join('templates', 'sensors_template.txt')
sensors_template = string.Template(pkg_resources.resource_string(resource_package, resource_path))

resource_path = os.path.join('templates', 'sensor_template.txt')
sensor_template = string.Template(pkg_resources.resource_string(resource_package, resource_path))


# Needed this since the output buffer wasn't getting written on raw_input on windows/msys
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)


# Setup argparser
parser = argparse.ArgumentParser()
parser.add_argument(
    '-v', '--verbose',
    help="Verbose logging",
    action="store_const", dest="loglevel", const=logging.INFO,
    default=logging.WARNING
)


subParsers = parser.add_subparsers(help="Available sub-commands", dest='command')

# Setup "run" subparser
runParser = subParsers.add_parser("run", help="Run the specified Gecko application")
runParser.add_argument(
    "application",
    help="Directory that contains your application"
)

runParser.add_argument(
    '-H', '--host',
    help="Set host to send requests to",
    action="store", dest="host", 
    default="https://m2.exosite.com"
)

# Setup "simulator" parser
simParser = subParsers.add_parser("simulate", help="Simulate data from simulation file")
simParser.add_argument(
    "simulator",
    help="Directory or file that contains definitions for your simulated data"
)

simParser.add_argument(
    '-H', '--host',
    help="Set host to send requests to",
    action="store", dest="host", 
    default="https://m2.exosite.com"
)



# Setup "init" subparser
initParser = subParsers.add_parser("init", help="Initialize a new gecko application") 
initParser.add_argument(
    "new_app_name",
    help="Name of the application that you want to create"
)

args = parser.parse_args()

# setup logger
logger = logging.getLogger('gecko')
logger.setLevel(args.loglevel)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


# uncomment this to get global logger (apscheduler uses this)
'''
aps = logging.getLogger()
aps.setLevel(logging.DEBUG)
aps.addHandler(ch)
'''


# Add cwd to path.  This allows us to find our app relative to where gecko command
# is ran from
import sys
sys.path.insert(1,'./')

def processJobError(event):
    global scheduler
    name = event.job_id
    j = scheduler.get_job(event.job_id)
    if j != None:
        # Add the name if we have it.  For the initial jobs that aren't store in the 
        # jobstore, we no longer have the name
        name = j.name
        
    logger.error("Error in job.  ID: " + name + " -- Traceback: " + event.traceback)
    
    
scheduler = None





def run(args):
    '''
    Run a gecko application
    '''
    global scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_listener(processJobError, apscheduler.events.EVENT_JOB_ERROR)
   

    # Check if arg was passed
    # Strip off trailing '/' that autocomplete would put in
    app = args.application.rstrip('/')
    try:
        app = importlib.import_module(app)
    except ImportError as e:
        # Check if the folder exists, if it does, add __init__ (if it doesn't exist)
        # and try again
        # Display error message
        logger.error("Error loading application: " + str(e))
        return
   
    # Create gecko core.  This goes and looks for connected gecko IO boards
    gecko = Gecko()
    
    # make sure app has sensors
    try:
        x = app.sensors
    except AttributeError as e:
        logger.error("App does not contain sensors.py file.")
        return
    things = app.sensors
    sensors = {}
    
    # Find all classes the subclass GeckoIO.I_O.Input
    for k, v in things.__dict__.items():
        a = inspect.isclass(v)
        if a:
            b = issubclass(v, GeckoIO.I_O.Input)
            if b:
                # Only add if we're a subclass of an input
                sensors[k] = v
            
    logger.info(sensors)
    for sensorname, sensor in sensors.iteritems():
        s = sensor()
        logger.info("Found sensor...")
        logger.info("    Name:        " + s.__class__.__name__)
        logger.info("    Description: " + s.description)
        logger.info("    Report rate: " + str(s.report_rate) + " seconds.")
        # make sure underlying sensor type exists
        if (issubclass(sensor, GeckoIO.Boards.ControlAnything.IO)) and (gecko.ControlAnything == None):
            logger.error("Tried to add a Control Anything sensor when no ControlAnything board was detected")
            return
        elif (issubclass(sensor, GeckoIO.Boards.GrovePi.IO)) and (gecko.GrovePi == None):
            logger.error("Tried to add a GrovePi sensor when no ControlAnything board was detected")
            return

        # add job for each sensor
        scheduler.add_job(sensor.getVal,  args = [s, gecko, args.host] ) # Run initial sensor grab right away
        scheduler.add_job(sensor.getVal, 'interval', args = [s, gecko, args.host], seconds=sensor.report_rate, max_instances=3, name=s.__class__.__name__)  # set job for future runs

    logger.info("Done adding sensors")
    scheduler.start()
    import time
    while (True):
        time.sleep(1)

import re


def init(args):
    print("Initializing new application " + args.new_app_name)
    # create folder
    cleanedAppName = re.sub(r'\W+', '', args.new_app_name).replace (" ", "_")
    if os.path.exists(cleanedAppName):
        response = ""
        while response == "":
            response = raw_input(cleanedAppName + " directory already exists.  Any duplicate files will be overwritten.\r\nAre you sure you want to recreate the application?  (Y/n)")

        if response.lower() == 'y' or response.lower() == 'yes':
            pass
        else:
            logger.error("Aborting new application creation")
            return
    else:
        os.makedirs(cleanedAppName)

    sensors = []
    addSensor = True
    while addSensor:
        # Let's just do 1 sensor that is an analog pin on a control anything board for now
        cleanedSensorName = raw_input("Enter the name of your sensor: ").replace (" ", "_")
        cleanedSensorName = re.sub(r'\W+', '', cleanedSensorName)


        # Get the pin number
        pinNumber = ""
        while not pinNumber.isdigit():
            pinNumber = raw_input("Enter the pin number your sensor is attached to: ")

        # Get the report rate
        reportRate = ""
        while not reportRate.isdigit():
            reportRate = raw_input("Enter the desired report rate (how often to send data to Exosite) in seconds: ")

        # Get the cik (This is a temporary thing
        cik = ""
        while (not all(c in string.hexdigits for c in cik)) or (len(cik) != 40):
            cik = raw_input("Enter the cik of your device: ")

        sensorInfo = {'sensor_name':cleanedSensorName, 
                      'board_type':'ControlAnything', 
                      'pin_number': pinNumber, 
                      'report_rate': reportRate,
                      'cik':cik}

        sensors.append(sensorInfo)

        response = ""
        while response == "":
            response = raw_input("Do you want to add another Sensor?  (Y/n)")

        if response.lower() == 'y' or response.lower() == 'yes':
            addSensor = True
        else:
            addSensor = False
    
    
    # compile all sensors into a single string
    sensorClasses = ""
    for sensor in sensors:
        sensorClasses = sensorClasses + sensor_template.substitute(sensor) + '\n'

    # Stuff sensors into sensors template
    sensorsFileContents = sensors_template.substitute({'sensors': sensorClasses})

    with open(cleanedAppName + "/sensors.py", 'w') as f:
        f.write(sensorsFileContents)

    # create init file
    
    with open(cleanedAppName + "/__init__.py", 'w') as f:
        f.write("import sensors")


def main():
    if args.command == "run":
        run(args)
    elif args.command == "init":
        init(args)
    elif args.command == "simulate":
        simulate(args)
    
   
   
    
    
    
   




if __name__ == "__main__":
    main()
