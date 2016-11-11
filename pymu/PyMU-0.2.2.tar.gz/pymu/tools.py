from .client import Client
from .pmuConfigFrame import ConfigFrame 
from .pmuCommandFrame import CommandFrame
from .aggPhasor import *
from .pmuDataFrame import *

MAXFRAMESIZE = 65535

## @brief Send command to turn off real-time data
#
# @param cli Client connection to data source
# @param idcode Frame ID
def turnDataOff(cli, idcode):
    '''
    Send DATA OFF command to data source

    @param cli: Client being used to connect to data source
    @param idcode: Frame ID of data source
    '''
    cmdOff = CommandFrame("DATAOFF", idcode)
    cli.sendData(cmdOff.fullFrameBytes)

## @brief Send command to turn on real-time data
#
# @param cli Client connection to data source
# @param idcode Frame ID
def turnDataOn(cli, idcode):
    cmdOn = CommandFrame("DATAON", idcode)
    cli.sendData(cmdOn.fullFrameBytes)

## @brief Request configframe from data source
#
# @param cli Client connection to data source
# @param idcode Frame ID
def requestConfigFrame2(cli, idcode):
    cmdConfig2 = CommandFrame("CONFIG2", idcode)
    cli.sendData(cmdConfig2.fullFrameBytes)

## @brief Read config frame from data source
#
# @param cli Client connection to data source
# @param debug Print debug statements
#
# @return Populated ConfigFrame object
def readConfigFrame2(cli, debug=False):
    configFame = None

    s = cli.readSample(4)
    configFrame = ConfigFrame(bytesToHexStr(s), debug)
    expSize = configFrame.framesize
    s = cli.readSample(expSize - 4)
    configFrame.frame = configFrame.frame + bytesToHexStr(s).upper()
    configFrame.finishParsing()

    return configFrame

## @brief Get a data sample regardless of TCP or UDP connection
#
# @parm rcvr Client or Server class element used for receiving data frames
#
# @return Data frame in hex string format
def getDataSample(rcvr, debug=False):

    fullHexStr = ""

    if type(rcvr) == "client":
        introHexStr = bytesToHexStr(rcvr.readSample(4))
        lenToRead = int(introHexStr[5:], 16)
        remainingHexStr = bytesToHexStr(rcvr.readSample(lenToRead))

        fullHexStr = introHexStr + remainingHexStr
    else:
        fullHexStr = bytesToHexStr(rcvr.readSample(64000))

    return fullHexStr

## @brief Connect to data source, request config frame, send data start command
#
# @param idcode Frame ID of PMU
# @param ip IP address of data source
# @param port Command port on data source
# @param tcpUdp Use TCP or UDP
# @param debug Print debug statements
#
# @return Populated ConfigFrame object
def startDataCapture(idcode, ip, port=4712, tcpUdp="TCP", debug=False):
    configFrame = None

    cli = Client(ip, port, tcpUdp)
    cli.setTimeout(5)
    
    while configFrame == None:
        #turnDataOff(cli, idcode)
        requestConfigFrame2(cli, idcode)
        configFrame = readConfigFrame2(cli, debug)

    turnDataOn(cli, idcode)
    cli.stop()

    return configFrame

## @brief Returns all station names from the config frame
#
# @param configFrame ConfigFrame containing stations
#
# @return List containing all the station names
def getStations(configFrame):
    stations = []
    for s in configFrame.stations:
        print("Station:", s.stn)
        stations.append(s)
    
    return stations

## @brief Creates an array of aggregate phasors for data collection
#
# @param configFrame ConfigFrame containing stations
#
# @return List containing all the station AggPhasor objects
def createAggPhasors(configFrame):
    pmus = []
    for s in getStations(configFrame):
        phasors = []
        print("Name:", s.stn)
        for p in range(0, s.phnmr):
            print("Phasor:", s.channels[p])
            theUnit = "VOLTS"
            if s.phunits[p].voltORcurr == "CURRENT":
                theUnit = "AMPS"
            phasors.append(AggPhasor(s.stn.strip() + "/" + s.channels[p].strip(), theUnit))

        pmus.append(phasors)
    
    return pmus

## @brief Takes in an array of dataFrames and inserts the data into an array of aggregate phasors
#
# @param data List containing all the data samples
# @param configFrame ConfigFrame containing stations
# @param pmus List of phasor values
#
# @return List containing all the phasor values
def parseSamples(data, configFrame, pmus):
    numOfSamples = len(data)
    for s in range(0, numOfSamples):
        for p in range(0, len(data[s].pmus)):
            for ph in range(0, len(data[s].pmus[p].phasors)):
                utcTimestamp = data[s].soc.utcSec + (data[s].fracsec / configFrame.time_base.baseDecStr) 
                pmus[p][ph].addSample(utcTimestamp, data[s].pmus[p].phasors[ph].mag, data[s].pmus[p].phasors[ph].rad)

    return pmus

