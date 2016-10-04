#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import threading
import sys

from collections import deque

# Constants
#VALUES_TO_PLOT = ['cwnd', 'sst', 'rtt', 'bw', 'loss'] # (only values for Y-axis)
# VALUES_TO_PLOT_ON_SECOND_AXIS = ['rtt']
VALUES_TO_PLOT = ['cwnd', 'sst', 'rtt', 'bw'] # (only values for Y-axis)
VALUES_TO_PROCESS = ['time']  + VALUES_TO_PLOT #helper to init all data structures

DEFAULT_LINES_TO_SHOW = ['cwnd']
DEFAULT_FILTER_PORT = 5001

LOG_FORMAT = ['time', 'rTime', 'srcIp', 'srcPort', 'dstIp', 'dstPort', 'cwnd', 'sst', 'rtt', 'minRtt', 'maxRtt', 'avgRtt', 'meanRtt', 'throughput', 'smoothedThroughput', 'assumedLosses']
#at least time & dstPort required
NUMBER_OF_VALUES = len(LOG_FORMAT)

THREAD_STOPFLAG_WAIT = 0.000001 # in seconds
THREAD_JOIN_TIMEOUT = 1 # in seconds
THREAD_TESTTIMEOUTS_WAIT = 0.5 # in seconds
THREAD_MISC_WAIT = 2 # in seconds

class TcpLivePlot():
    def __init__(self, inputBackend, outputBackend, options, infoRegistry):
        self.inputBackend = inputBackend
        self.outputBackend = outputBackend
        self.options = options
        self.infoRegistry = infoRegistry

        self.__stopped = threading.Event()
        self.__processInputThread = None
        self.__processInputFilteringThread = None
        self.__processGuiThread = None

        # initialize vars
        self.incomeBuffer = deque(maxlen=self.options.bufferLength)
        self.connectionBuffer = {}
        self.__tmpTimestamp = 0

        self.outputBackend.setConnectionBuffer(self.connectionBuffer)

        if(len(self.options.filterPorts) < 1):
            self.options.filterPorts.append(DEFAULT_FILTER_PORT)
        # for i in self.options.filterPorts:
        #     self.__connectionBuffer[i] = deque(maxlen=self.options.bufferLength)

        # init threads
        self.__processInputThread = threading.Thread(target=self.processInput)
        # self.__processInputFilteringThread= threading.Thread(target=self.processInputFiltering)
        self.__processGuiThread = threading.Thread(target=self.processGui)
        self.__processInputThread.daemon = True
        # self.__processInputFilteringThread.daemon = True
        self.__processGuiThread.daemon = True
        self.__processInputThread.start()
        # self.__processInputFilteringThread.start()
        # self.__processGuiThread.start()

        while(not self.__stopped.wait(THREAD_STOPFLAG_WAIT)):
            # self.__stopped.wait(0.5)
            self.processGui()

        if(self.options.debug):
            print("End of main thread reached.")


    def processInput(self):
        """
        Thread reads from input sources (socket/file/stdin)
        """
        while(not self.__stopped.wait(THREAD_STOPFLAG_WAIT)):
            newSamples = self.inputBackend.retrieveNewSamples()
            for sample in newSamples:
                tmpData = sample.split(" ")
                if(len(tmpData) == len(LOG_FORMAT)):
                    data = dict(zip(LOG_FORMAT, tmpData))
                    # print(data)
                    port = int(data['dstPort'])
                    if(port not in self.connectionBuffer):
                        self.connectionBuffer[port] = deque()
                    self.connectionBuffer[port].append(data)
                    # self.incomeBuffer.append(sample)

    def processGui(self):
        # while(not self.__stopped.wait(THREAD_STOPFLAG_WAIT)):
        #     try:
        #         line = self.incomeBuffer.popleft()
        #     except IndexError:
        #         pass
        #     else:
        # import matplotlib.pyplot as plt
        self.outputBackend.plotGraph()
        # plt.show()


    def processInputFiltering(self):
        """
        Filters retrieved data by selected port. Drops malformed data.
        """
        return

        lastTimestamp = 0
        while(True):
            try:
                line = self.incomeBuffer.popleft()
            except IndexError:
                time.sleep(0.00001)
            else:
                tmpData = line.split(" ")
                if(len(tmpData) is NUMBER_OF_VALUES):
                    data = dict(zip(LOG_FORMAT, tmpData))
                else:
                    continue

                try:
                    timestamp = float(data['time'])
                    port = int(data['dstPort'])
                except ValueError:
                    continue
                else:
                    if(port not in self.options.filterPorts):
                        continue

                filteredData = {}
                try:
                    for val in VALUES_TO_PROCESS:
                        filteredData[val] = float(data[val])
                except ValueError:
                    continue
                else:
                    timestampDelta = lastTimestamp - timestamp
                    if(timestampDelta > self.options.plotResolution):
                        lastTimestamp = timestamp
                        continue
                    self.connectionBuffer[port].append(filteredData)
                    lastTimestamp = timestamp

    def handleSignals(self, signal, frame):
        """
        Callback handler for signals
        """
        if(not self.options.quiet and not self.options.outputBackend == 'stdout'):
            print("Exiting...")
        self.initTearDown()
        self.tearDown()
        raise SystemExit
        sys.exit(0)

    def initTearDown(self):
        """
        Sets stops signal for all threads.
        """
        self.__stopped.set()

    def tearDown(self):
        """
        Performs the cleanup at programm termination.
        """
        self.inputBackend.tearDown()
        self.outputBackend.tearDown()
