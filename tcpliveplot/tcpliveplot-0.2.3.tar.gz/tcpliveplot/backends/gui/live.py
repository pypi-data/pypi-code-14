# -*- coding: utf-8 -*-

# TODO:
# * dynamic flow detection
# * flowIdentifer i/o "port"
# * fix socket-input
# * dynamic value detection

import numpy as np

import math
import sys
import time
import threading
from collections import deque
from .gui_base import GuiBase

VALUES_TO_PLOT = ['cwnd', 'sst', 'rtt', 'smoothedThroughput'] # (only values for Y-axis)
VALUES_TO_PROCESS = ['time']  + VALUES_TO_PLOT #helper to init all data structures

# Strings for UI-elements
FIGURE_TITLE = "TCPplot"
PLOT_TITLE = "Data from"
PAUSE = "Pause"
QUIT = "Quit"

import matplotlib
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import matplotlib.animation as animation
from matplotlib.widgets import Button, RadioButtons

# constants
CLEAR_GAP = 0.2 # gap in s
INFINITY_THRESHOLD = 1e8

class LiveGui(GuiBase):
    def __init__(self, options, infoRegistry):
        self.options = options
        self.infoRegistry = infoRegistry
        self.__stopped = threading.Event()
        self.timestampOfLastGuiRefresh = 0

        if(self.options.debug):
            print("matplotlib-version: " +  matplotlib.__version__)
            print("available matplotlib-styles:" + str(plt.style.available))


    def setConnectionBuffer(self, connectionBuffer):
        self.__connectionBuffer = connectionBuffer

    def tearDown(self):
        plt.close()
        sys.exit(0)
        pass

    def startUp(self):
        pass

    def startupCheck(self):
        pass

    def pause(self, event):
        """Toggles pause flag."""
        self.__paused ^= True
        return

    def toggleVisibility(self, lineID):
        """Toggles visibility for given line."""
        for port in self.options.filterPorts:
            self.__plotLineConfigs[port][lineID] ^= True
            self.__plotLines[port][lineID].set_visible(self.__plotLineConfigs[port][lineID])
        self.drawPlotLegend()


    def updateValueVisibility(self, label):
        for port in self.options.filterPorts:
            for i in range(1, len(VALUES_TO_PLOT)+1):
                self.__plotLineConfigs[port][VALUES_TO_PLOT[(i-1)]] = False
                self.__plotLines[port][(VALUES_TO_PLOT[(i-1)])].set_visible(self.__plotLineConfigs[port][(VALUES_TO_PLOT[(i-1)])])
        if label == 'cwnd':
            self.toggleVisibility(VALUES_TO_PLOT[0])
        elif label == 'sst':
            self.toggleVisibility(VALUES_TO_PLOT[1])
        elif label == 'rtt':
            self.toggleVisibility(VALUES_TO_PLOT[2])
        elif label == 'bw':
            self.toggleVisibility(VALUES_TO_PLOT[3])
        else:
            pass

    def drawPlotLegend(self):
        """(Re)draws legend with visible lines."""
        labelObjs  = []
        labelTexts = []
        for port in self.options.filterPorts:
            for val in VALUES_TO_PLOT:
                if(self.__plotLineConfigs[port][val]):
                    labelObjs.append(self.__plotLines[port][val])
                    labelTexts.append(self.__plotLines[port][val].get_label())
        if(len(labelObjs) > 0):
            self.__ax.legend(labelObjs, labelTexts, fontsize='small')
        else:
            self.__ax.legend_.remove()

    def plotKeyPressCallback(self, event):
        """Callback to handle key presses."""
        if(self.options.debug):
            print("Key pressed: '" + event.key + "'")

        # p pauses
        if(event.key == "p"):
            self.pause(event)
        # ctrl+{c,q,w} quits programm
        elif(event.key == "ctrl+c" or event.key == "ctrl+w" or event.key == "ctrl+q"):
            raise SystemExit
        else:
            try:
                index = int(event.key)
            except ValueError:
                pass
            else:
                # Numbers 1-N toggle visibility of lines
                if index in range(1, len(VALUES_TO_PLOT)+1):
                    self.toggleVisibility(VALUES_TO_PLOT[(index-1)])

    def stopPlotting(self, event):
        """Callback function to stop plotting and the programm."""
        self.__tmpTimestamp = time.perf_counter()
        self.tearDown()

    def plotGraph(self):
        """Initializes plot configuration and starts the plotting."""
        self.__paused = False
        self.__minVal = 9999999999
        self.__maxVal = 0

        fig = plt.figure(FIGURE_TITLE)
        fig.canvas.mpl_connect('key_press_event', self.plotKeyPressCallback)
        self.__ax = plt.axes()
        # self.__ax2 = self.__ax.twinx()
        self.__ax.set_autoscaley_on(False)
        self.__ax.set_xlim(0, self.options.xDelta)
        self.__ax.set_title(PLOT_TITLE + " :" + ', :'.join(map(str, self.options.filterPorts)))

        self.__plotLines = {}
        self.__plotValues = {}
        self.__plotValuesMin = {}
        self.__plotValuesMax = {}
        self.__plotLineConfigs = {}
        for port in self.options.filterPorts:
            self.__plotLines[port] = {}
            self.__plotValues[port] = {}
            self.__plotValuesMin[port] = {}
            self.__plotValuesMax[port] = {}
            self.__plotLineConfigs[port] = {}
            self.__plotLineConfigs[port]['lastTimestamp'] = 0
            for val in VALUES_TO_PROCESS:
                self.__plotValuesMin[port][val] = math.inf
                self.__plotValuesMax[port][val] = -math.inf
                self.__plotValues[port][val] = deque(maxlen=(int(self.options.xDelta / self.options.plotResolution * 10)))
            index = 1
            for val in VALUES_TO_PLOT:
                # if(val == "rtt"):
                #     print("bla")
                #     self.__plotLines[port][val], = self.__ax2.plot([])
                # else:
                self.__plotLines[port][val], = self.__ax.plot([])
                self.__plotLines[port][val].set_label("[" + str(index) + "] " + val + " - " + str(port) + "")
                self.__plotLineConfigs[port][val] = True
                self.__plotLines[port][val].set_visible(True)
                index += 1
        self.drawPlotLegend()

        # pause button
        pauseAx = plt.axes([0.8, 0.025, 0.1, 0.04])
        pauseButton = Button(pauseAx, PAUSE)
        pauseButton.on_clicked(self.pause)

        # quit button
        quitAx = plt.axes([0.125, 0.025, 0.1, 0.04])
        quitButton = Button(quitAx, QUIT)
        quitButton.on_clicked(self.stopPlotting)


        # valueCheckboxesAx = plt.axes([0.05, 0.4, 0.1, 0.15])
        # valueCheckboxes = CheckButtons(valueCheckboxesAx, ('cwnd', 'sst', 'rtt', 'bw'), (True, False, False, False))
        # valueCheckboxes.on_clicked(self.updateValueVisibility)

        # valueRadiobuttonsAx = plt.axes([0.020, 0.025, 0.075, 0.15])
        # valueRadiobuttons = RadioButtons(valueRadiobuttonsAx, ('cwnd', 'sst', 'rtt', 'bw'))
        # valueRadiobuttons.on_clicked(self.updateValueVisibility)

        if(self.options.preloadBuffer > 0):
            self.__preloading = True
        else:
            self.__preloading = False

        self.__lastPlotTimestamp = {}
        for port in self.options.filterPorts:
            self.__lastPlotTimestamp[port] = 0
        self.__lastDrawTimestamp = 0
        self.__initRealtimeTimestamp = 0
        self.__initSampletimeTimestamp = -1

        self.__timeOffset = 0
        self.__bufferFactor = 1
        self.__apsFixFactor = 1

        # call update-routine
        # self.plotInit()
        # self.__plotLine = self.plotGraphUpdate(0)
        animation.FuncAnimation(fig, self.plotGraphUpdate, init_func=self.plotInit, frames=self.options.drawFps, interval=self.options.drawIntervall, blit=self.options.blitting, repeat=True)
        # if self.__stopped.isSet():
        #     return
        # else:
        # plt.ioff()
        # plt.draw()
        plt.show()
        # print("bar")

    def returnAllLines(self):
        """Macro to return all lines as they are."""
        allPlotLines = []
        for port in self.options.filterPorts:
            for val in VALUES_TO_PLOT:
                allPlotLines.append(self.__plotLines[port][val])
        return tuple(allPlotLines)

    def returnNanSample(self, time):
        """Macro to return NaN-Samples (to fill plot)."""
        data = {}
        data['time'] = time - self.options.plotResolution
        for val in VALUES_TO_PLOT:
            data[val] = np.nan
        return data

    def plotGraphUpdate(self, i):
        """Animation loop - does the actual plot update."""
        if(self.__initSampletimeTimestamp == -1):
            self.__initSampletimeTimestamp = 0
            return self.returnAllLines()
        elif(self.__initSampletimeTimestamp == 0):
            self.calculateSampleTimeOffset()
            return self.returnAllLines()

        # fill playback-buffer
        if(False and self.__preloading):
            bufferLength = -1
            for port in self.options.filterPorts:
                bufferLength = max(bufferLength, len(self.__connectionBuffer[port]))

            if(bufferLength > 0):
                bufferedTime = bufferLength * self.options.plotResolution
                bufferTarget = self.options.preloadBuffer * self.__bufferFactor
                if(bufferedTime >= bufferTarget):
                    self.__preloading = False
                    # reduce buffer-target to half size after initial buffering
                    self.__bufferFactor = 0.5
                    print("Buffer filled.")
            if(self.__preloading):
                print("Buffering... " + str(format(bufferedTime, ".2f")) + "/" + str(format(bufferTarget, ".2f")))
                return self.returnAllLines()

        if(self.__paused == True):
            return self.returnAllLines()
        else:
            while(True):
                currentTimestamp = time.perf_counter()
                if(self.__initRealtimeTimestamp == 0):
                    self.__initRealtimeTimestamp = currentTimestamp
                timestampDelta = (currentTimestamp - self.__lastDrawTimestamp) * self.options.playbackSpeed * self.__apsFixFactor

                currentXmin, currentXmax = self.__ax.get_xlim()
                currentYmin, currentYmax = self.__ax.get_ylim()
                newXmax = currentTimestamp - self.options.preloadBuffer
                newXmin = newXmax - self.options.xDelta
                self.__ax.set_xlim(newXmin, newXmax)

                maxYval = -math.inf
                minYval = math.inf
                connectionsData = {}

                # skip this cycle, plot resolution not yet reached
                if(timestampDelta < self.options.plotResolution):
                    return self.returnAllLines()

                for port in self.options.filterPorts:
                    connectionsData[port] = deque()
                    whileRun = True
                    while(len(self.__connectionBuffer[port]) > 0 and whileRun):
                        try:
                            data = self.__connectionBuffer[port].popleft()
                        except IndexError:
                            whileRun = False
                            pass
                        else:
                            lineTime = self.__initRealtimeTimestamp  + (float(data['time']) - self.__initSampletimeTimestamp)
                            # time in past
                            if(lineTime < newXmin):
                                continue
                            # time older than newst timestamp
                            elif(lineTime < self.__lastPlotTimestamp[port]):
                                continue
                            # skip this sample due plot plotResolution
                            elif((lineTime - self.__lastPlotTimestamp[port]) < self.options.plotResolution):
                                continue
                            else:
                                if(self.__lastPlotTimestamp[port] > 0 and ((lineTime - self.__lastPlotTimestamp[port]) > CLEAR_GAP)):
                                    self.__lastPlotTimestamp[port] = lineTime
                                    nanSample = self.returnNanSample(lineTime)
                                    connectionsData[port].append(nanSample)
                                infinityReached = False
                                for val in VALUES_TO_PLOT:
                                    try:
                                        convertedValue = float(data[val])
                                    except ValueError:
                                        data[val] = np.nan
                                    else:
                                        if(convertedValue > INFINITY_THRESHOLD):
                                            data[val] = np.nan
                                        # nanSample = self.returnNanSample(lineTime)
                                        # connectionsData[port].append(nanSample)
                                        # infinityReached = True

                                if(not infinityReached):
                                    self.__lastPlotTimestamp[port] = lineTime
                                    connectionsData[port].append(data)

                data = 0
                for port in connectionsData:
                    if(len(connectionsData[port]) > 0):
                        data += 1

                for port in self.options.filterPorts:
                    if(data < 1 and currentTimestamp > self.__lastPlotTimestamp[port] ):
                        if(self.options.debug):
                            print("No data for any connection.")
                        if(self.options.interimBuffering):
                            self.__preloading = True
                        return self.returnAllLines()



                # copy raw-value into corresponding lists
                for connection in connectionsData:
                    while(len(connectionsData[connection]) > 0):
                        data = connectionsData[connection].popleft()

                        lineTime = self.__initRealtimeTimestamp  + (float(data['time']) - self.__initSampletimeTimestamp)
                        self.__plotLineConfigs[connection]['lastTimestamp'] = float(data['time'])

                        for val in VALUES_TO_PROCESS:
                            if(val == 'time'):
                                self.__plotValues[connection][val].append(lineTime)
                            else:
                                try:
                                    currentVal = float(data[val])
                                except ValueError:
                                    pass
                                else:
                                    self.__plotValues[connection][val].append(currentVal)

                    # update axis (xy-tuple) with data from lists
                    for val in VALUES_TO_PLOT:
                        x, y = self.__plotValues[connection]['time'], self.__plotValues[connection][val]
                        self.__plotLines[connection][val].set_data(x, y)


                self.__lastDrawTimestamp = time.perf_counter()

                # y-scaling
                lines = self.__ax.get_lines()
                bot,top = np.inf, -np.inf
                for line in lines:
                    if(line.get_visible()):
                        new_bot, new_top = self.determineNewYvalues(line)

                        if(new_bot != new_top):
                            if(new_bot < bot):
                                bot = new_bot
                            if(new_top > top):
                                top = new_top

                if(bot != np.inf and top != -np.inf):
                    self.__ax.set_ylim(bot, top)
                else:
                    # intial y-scale
                    self.__ax.set_ylim(0, 500)

                return self.returnAllLines()

    def determineNewYvalues(self, line, margin=0.25):
        xLine = line.get_xdata()
        yLine = line.get_ydata()
        xData = np.array(xLine)
        yData = np.array(yLine)
        low,high = self.__ax.get_xlim()
        yVisibleMask = yData[((xData>low) & (xData<high))]
        if(len(yVisibleMask) > 0):
            height = np.max(yVisibleMask) - np.min(yVisibleMask)
            bot = np.min(yVisibleMask) - margin * height
            top = np.max(yVisibleMask) + margin * height
            return bot,top
        else:
            return 0,0

    def plotInit(self):
        """Helper to initialize plot."""
        for port in self.options.filterPorts:
            for val in VALUES_TO_PLOT:
                self.__plotLines[port][val].set_data([], [])

        newXmin = 0
        newXmax = newXmin + self.options.xDelta
        self.__ax.set_xlim(newXmin, newXmax)

        # if(self.options.debug):
        #     print("Plot init done.")

        return self.returnAllLines()

    def calculateSampleTimeOffset(self):
        """Calculate SampleTime difference at start"""
        for port in self.options.filterPorts:
            try:
                data = self.__connectionBuffer[port].popleft()
            except IndexError:
                pass
            except KeyError:
                pass
            else:
                # print(data)
                #re-add first sample (to head of dequeue)
                self.__connectionBuffer[port].appendleft(data)
                self.__initSampletimeTimestamp = float(data['time'])
                return

