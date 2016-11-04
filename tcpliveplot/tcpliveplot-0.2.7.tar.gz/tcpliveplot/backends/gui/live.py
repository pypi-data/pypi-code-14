# -*- coding: utf-8 -*-

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
        self.__lastPlotTimestamp = {}
        self.__lastDrawTimestamp = 0
        self.__initRealtimeTimestamp = 0
        self.__initSampletimeTimestamp = -1
        self.xmin = 0
        self.xmax = self.xmin + self.options.xDelta
        self.flows = []
        self.lineVisibility = {}

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
        for val in VALUES_TO_PLOT:
            if((len(self.options.initialLineVisibility) < 1) or (val in self.options.initialLineVisibility)):
                self.lineVisibility[val] = True
            else:
                self.lineVisibility[val] = False

    def pause(self, event):
        """Toggles pause flag."""
        self.__paused ^= True
        return

    def toggleVisibility(self, lineID):
        """Toggles visibility for given line."""
        self.lineVisibility[lineID] ^= True
        for flowIdentifier in self.__connectionBuffer:
            if(flowIdentifier in self.flows and flowIdentifier in self.__plotLineConfigs):
                self.__plotLineConfigs[flowIdentifier][lineID] ^= True
                self.__plotLines[flowIdentifier][lineID].set_visible(self.__plotLineConfigs[flowIdentifier][lineID])
        self.drawPlotLegend()


    def updateValueVisibility(self, label):
        for flowIdentifier in self.__connectionBuffer:
            for i in range(1, len(VALUES_TO_PLOT)+1):
                if(flowIdentifier in self.flows and flowIdentifier in self.__plotLineConfigs):
                    self.__plotLineConfigs[flowIdentifier][VALUES_TO_PLOT[(i-1)]] = False
                    self.__plotLines[flowIdentifier][(VALUES_TO_PLOT[(i-1)])].set_visible(self.__plotLineConfigs[flowIdentifier][(VALUES_TO_PLOT[(i-1)])])
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
        if len(self.__connectionBuffer) > 0:
            labelObjs  = []
            labelTexts = []
            for flowIdentifier in self.__connectionBuffer:
                if(flowIdentifier in self.flows and flowIdentifier in self.__plotLineConfigs):
                    for val in VALUES_TO_PLOT:
                        if(self.__plotLineConfigs[flowIdentifier][val]):
                            labelObjs.append(self.__plotLines[flowIdentifier][val])
                            labelTexts.append(self.__plotLines[flowIdentifier][val].get_label())
            if(len(labelObjs) > 0):
                self.legendVisible = True
                self.__ax.legend(labelObjs, labelTexts, fontsize='small')
            else:
                if self.legendVisible:
                    self.legendVisible = False
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

    def updateFlowDataStructures(self):
        # test all flows if outdated and replace list in-place
        for flowIdentifier in self.flows:
            self.flows[:] = [i for i in self.flows if not self.isFlowOutdated(i)]

        for flowIdentifier in self.__connectionBuffer:
            if(flowIdentifier not in self.flows):
                self.initFlowDataStructures(flowIdentifier)

        self.drawPlotLegend()

    def isFlowOutdated(self, flowIdentifier):
        outdated = self.__lastPlotTimestamp[flowIdentifier] < self.xmin
        if(outdated):
            for val in VALUES_TO_PLOT:
                self.__plotLineConfigs[flowIdentifier][val] = False
                self.__plotLines[flowIdentifier][val].set_visible(False)
                self.__plotLines[flowIdentifier][val].set_data([], [])
                self.__plotValues[flowIdentifier][val] = []
            self.drawPlotLegend()

    def initFlowDataStructures(self, flowIdentifier):
        splittedFlowidentifier = flowIdentifier.split("-")
        srcPort = splittedFlowidentifier[0]
        dstPort = splittedFlowidentifier[1]
        dstPortCount = 1
        for preexistingFlow in self.flows:
            flowDstPort = preexistingFlow.split("-")[1]
            if flowDstPort == dstPort:
                dstPortCount += 1

        self.flows.append(flowIdentifier)
        self.__lastPlotTimestamp[flowIdentifier] = 0
        self.__plotLines[flowIdentifier] = {}
        self.__plotValues[flowIdentifier] = {}
        self.__plotValuesMin[flowIdentifier] = {}
        self.__plotValuesMax[flowIdentifier] = {}
        self.__plotLineConfigs[flowIdentifier] = {}
        self.__plotLineConfigs[flowIdentifier]['lastTimestamp'] = 0
        for val in VALUES_TO_PROCESS:
            self.__plotValuesMin[flowIdentifier][val] = math.inf
            self.__plotValuesMax[flowIdentifier][val] = -math.inf
            self.__plotValues[flowIdentifier][val] = deque(maxlen=(int(self.options.xDelta / self.options.plotResolution * 10)))
        index = 1
        for val in VALUES_TO_PLOT:
            self.__plotLines[flowIdentifier][val], = self.__ax.plot([])
            self.__plotLines[flowIdentifier][val].set_label("[" + str(index) + "] " + val + " - " + str(dstPort) + " #" + str(dstPortCount) + "")
            self.__plotLineConfigs[flowIdentifier][val] = self.lineVisibility[val]
            self.__plotLines[flowIdentifier][val].set_visible(self.lineVisibility[val])
            self.__plotLines[flowIdentifier][val].set_data([], [])
            index += 1

    def destroyFlowDataStructures(self, flowIdentifier):
        self.flows.remove(flowIdentifier)
        # del(self.flows[(self.flows.index(flowIdentifier))])
        print("deleting " + str(flowIdentifier))

    def plotGraph(self):
        """Initializes plot configuration and starts the plotting."""

        while(len(self.__connectionBuffer) < 1):
            print("waiting for data on filtered flows...")
            time.sleep(0.5)

        if(self.options.debug):
            print("initializing...")
        time.sleep(1)


        self.__paused = False
        self.__minVal = 9999999999
        self.__maxVal = 0

        fig = plt.figure(self.options.title)
        fig.canvas.mpl_connect('key_press_event', self.plotKeyPressCallback)
        self.__ax = plt.axes()
        # self.__ax2 = self.__ax.twinx()
        self.__ax.set_autoscaley_on(False)
        self.__ax.set_xlim(0, self.options.xDelta)
        # self.__ax.set_title(PLOT_TITLE + " :" + ', :'.join(map(str, self.options.filterPorts)))
        self.__ax.set_title(self.options.title)

        self.__plotLines = {}
        self.__plotValues = {}
        self.__plotValuesMin = {}
        self.__plotValuesMax = {}
        self.__plotLineConfigs = {}

        self.updateFlowDataStructures()

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
        for flowIdentifier in self.__connectionBuffer:
            for val in VALUES_TO_PLOT:
                allPlotLines.append(self.__plotLines[flowIdentifier][val])
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

        self.updateFlowDataStructures()

        if(self.__initSampletimeTimestamp == -1):
            self.__initSampletimeTimestamp = 0
            return self.returnAllLines()
        elif(self.__initSampletimeTimestamp == 0):
            self.calculateSampleTimeOffset()
            return self.returnAllLines()

        # fill playback-buffer
        if(False and self.__preloading):
            bufferLength = -1
            for flowIdentifier in self.__connectionBuffer:
                bufferLength = max(bufferLength, len(self.__connectionBuffer[flowIdentifier]))

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
                self.xmin = newXmin
                self.xmax = newXmax
                self.__ax.set_xlim(newXmin, newXmax)

                maxYval = -math.inf
                minYval = math.inf
                connectionsData = {}

                # skip this cycle, plot resolution not yet reached
                if(timestampDelta < self.options.plotResolution):
                    return self.returnAllLines()

                for flowIdentifier in self.__connectionBuffer:
                    connectionsData[flowIdentifier] = deque()
                    whileRun = True
                    while(len(self.__connectionBuffer[flowIdentifier]) > 0 and whileRun):
                        try:
                            data = self.__connectionBuffer[flowIdentifier].popleft()
                        except IndexError:
                            whileRun = False
                            pass
                        else:
                            if(flowIdentifier not in self.flows):
                                continue

                            try:
                                dataTime = float(data['time'])
                            except ValueError:
                                continue
                            else:
                                lineTime = self.__initRealtimeTimestamp  + (dataTime - self.__initSampletimeTimestamp)

                            # time in past
                            if(lineTime < newXmin):
                                continue
                            # time older than newst timestamp
                            elif(lineTime < self.__lastPlotTimestamp[flowIdentifier]):
                                continue
                            # skip this sample due plot plotResolution
                            elif((lineTime - self.__lastPlotTimestamp[flowIdentifier]) < self.options.plotResolution):
                                continue
                            else:
                                if(self.__lastPlotTimestamp[flowIdentifier] > 0 and ((lineTime - self.__lastPlotTimestamp[flowIdentifier]) > CLEAR_GAP)):
                                    self.__lastPlotTimestamp[flowIdentifier] = lineTime
                                    nanSample = self.returnNanSample(lineTime)
                                    connectionsData[flowIdentifier].append(nanSample)
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
                                    self.__lastPlotTimestamp[flowIdentifier] = lineTime
                                    connectionsData[flowIdentifier].append(data)

                data = 0
                for flowIdentifier in connectionsData:
                    if(len(connectionsData[flowIdentifier]) > 0 and len(self.flows) > 0 and flowIdentifier in self.flows):
                        data += 1

                for flowIdentifier in self.__connectionBuffer:
                    if(data < 1 and currentTimestamp > self.__lastPlotTimestamp[flowIdentifier] ):
                        if(self.options.debug):
                            print("No data for any connection.")
                        return self.returnAllLines()



                # copy raw-value into corresponding lists
                for connection in connectionsData:
                    while(len(connectionsData[connection]) > 0):
                        data = connectionsData[connection].popleft()


                        try:
                            dataTime = float(data['time'])
                        except ValueError:
                            continue
                        else:
                            lineTime = self.__initRealtimeTimestamp  + (dataTime - self.__initSampletimeTimestamp)
                            self.__plotLineConfigs[connection]['lastTimestamp'] = dataTime

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

                if(self.options.yAxisMax is 0):
                    # y-scaling (autoscaling)
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
                else:
                    # static y-axis (no autoscaling)
                    self.__ax.set_ylim(0, self.options.yAxisMax)

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
        for flowIdentifier in self.__connectionBuffer:
            for val in VALUES_TO_PLOT:
                self.__plotLines[flowIdentifier][val].set_data([], [])


        newXmin = 0
        newXmax = newXmin + self.options.xDelta
        self.__ax.set_xlim(newXmin, newXmax)

        # if(self.options.debug):
        #     print("Plot init done.")

        return self.returnAllLines()

    def calculateSampleTimeOffset(self):
        """Calculate SampleTime difference at start"""
        for flowIdentifier in self.__connectionBuffer:
            try:
                data = self.__connectionBuffer[flowIdentifier].popleft()
            except IndexError:
                pass
            except KeyError:
                pass
            else:
                # print(data)
                #re-add first sample (to head of dequeue)
                self.__connectionBuffer[flowIdentifier].appendleft(data)
                try:
                    dataTime = float(data['time'])
                except ValueError:
                    continue
                else:
                    self.__initSampletimeTimestamp = dataTime
                return

