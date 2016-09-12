﻿from os import listdir
import json
import requests
import apscheduler
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import sys
import random
import math

scheduler = None

dataToSend = {}

simulators = []

host = None

logger = logging.getLogger('gecko')

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
'''
aps = logging.getLogger()
aps.setLevel(logging.DEBUG)
aps.addHandler(ch)
'''


USER_AGENT = 'GECKO_SIM'
EXOSITE_SERVER_URL = 'https://m2.exosite.com/'

TIMEOUT_SECONDS = 15

class Http_Response():
    def __init__(self, responseCode, responseBody):
        self.code = responseCode
        self.body = responseBody

def send_post(url, headers, data):
    try:
        response = requests.post(url, data=data, headers=headers,timeout=TIMEOUT_SECONDS, verify=True)
    except Exception as e:
        return Http_Response(0, str(e))
        
    return Http_Response(response.status_code, response.text)


def exosite_write(cik, data):
    headers = { 'User-Agent' : USER_AGENT, 
                'X-Exosite-CIK' : cik,
                'Content-Type' : 'application/x-www-form-urlencoded; charset=utf-8',
                }
    url= EXOSITE_SERVER_URL + 'onep:v1/stack/alias'

    return send_post(url, headers, data)



def processJobError(event):
    global scheduler
    name = event.job_id
    j = scheduler.get_job(event.job_id)
    if j != None:
        # Add the name if we have it.  For the initial jobs that aren't store in the 
        # jobstore, we no longer have the name
        name = j.name
        
    logger.error("Error in job.  ID: " + name + " -- Traceback: " + event.traceback)

class SimulatedData():
    # Represents one or many sensors that all have the same auth to Exosite.
    @staticmethod
    def getNextData(sensor, tickNumber):
        if sensor['type'] == 'linear':
            return sensor['data_characteristics']['slope']*tickNumber + sensor['data_characteristics']['offset']
        elif sensor['type'] == 'sinusoidal':
            # Period is set to seconds in a radian
            radianPerSec = 2*math.pi/sensor['data_characteristics']['period']
            radians = tickNumber * radianPerSec
            return round(math.sin(radians)*sensor['data_characteristics']['amplitude'] + sensor['data_characteristics']['offset'], 4)
        elif sensor['type'] == 'random':
            return random.uniform(sensor['data_characteristics']['min'], sensor['data_characteristics']['max'])
        elif sensor['type'] == 'open_weather_map':
            params = {
                "id": 5037649,
                "APPID": "787e3af70cc1a7d2a3b370a6f856eba3",
                "units": 'imperial'
                }
            res = requests.get("http://api.openweathermap.org/data/2.5/weather", params=params)
            if res.status_code == 200:
                obj = json.loads(res.content)
                return obj['main']['temp']


        raise("Unsupported simulator data type: " + sensor['type'])

    def __init__(self, sensors, auth):
        self.sensors = []
        self.auth = auth
        for sensor in sensors:
            sensor['simulated_data']['nextRunTick'] = 0
                
            self.sensors.append(sensor['simulated_data'])

    def tick(self, tickNumber):
        dataToSend={}
        for sensor in self.sensors:
            val = SimulatedData.getNextData(sensor, tickNumber)
            if tickNumber >= sensor['nextRunTick']:
                # interval hit
                sensor['nextRunTick'] = tickNumber + sensor['report_rate']
                dataToSend[sensor['name']] = val
                print(str(sensor['name']) + " -- " + str(val))

        if len(dataToSend) > 0:
            exosite_write(self.auth, dataToSend)
            print("sending data")
        


globalTicks = 0

def checkSensors():
    global globalTicks
    for simulator in simulators:
        simulator.tick(globalTicks)
        globalTicks = globalTicks + 1




def simulate(args):
    '''
    Simulate data
    '''
    #logger.setLevel(args.loglevel)
    global host
    host = args.host
    # Get simulated data files.
    files = {}
    if args.simulator.endswith('.json'):
        with open(args.simulator, 'r') as f:
            contents = f.read()
            try:
                files[args.simulator] = json.loads(contents)
            except Exception as e:
                logger.error("Error reading " + args.simulator + " -- " + str(e))
    else:
        for file in listdir(args.simulator):
            if file.endswith('.json'):
                with open(args.simulator + "/" + file, 'r') as f:
                    contents = f.read()
                    try:
                        files[file] = json.loads(contents)
                    except Exception as e:
                        logger.error("Error reading " + str(file) + " -- " + str(e))
    
    for file, values in files.iteritems():
        simulators.append(SimulatedData(values['sensors'], values['sensor_auth']))

    global scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_listener(processJobError, apscheduler.events.EVENT_JOB_ERROR)

    scheduler.add_job(checkSensors ) # Run initial sensor grab right away
    scheduler.add_job(checkSensors, 'interval', seconds=1, max_instances=3, name="sensor_check")  # set job for future runs


    scheduler.start()
    import time
    while (True):
        time.sleep(1)