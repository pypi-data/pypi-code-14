
from PySide.QtGui import QTreeView, QStandardItemModel, QStandardItem
from PySide.QtCore import Qt, QMutex

import sys

from karmadbg.dbgcore.util import showexception

from karmadbg.uicore.basewidgets import *
from karmadbg.uicore.async import *

import karmadbg.scripts.proclist as proclist

class ThreadProcessItem(QStandardItem):

    def __init__(self, uimanager, *args, **kwargs):
        super(ThreadProcessItem,self).__init__(*args, **kwargs)
        self.uimanager = uimanager

    def onDoubleClick(self):
        raise StopIteration


class ThreadItem(ThreadProcessItem):

    def __init__(self, threadInfo, uimanager):
        super(ThreadItem,self).__init__(uimanager)
        self.setEditable(False)
        self.tid = threadInfo.tid
        self.pid = threadInfo.pid
        self.kernel = threadInfo.isKernel
        self.targetId = threadInfo.targetId;

    def update(self, threadInfo):

        text = "* " if threadInfo.isCurrent else "  "

        if self.kernel:
            text += "CPU%d:  %s" % (threadInfo.tid, threadInfo.ip)
        else:
            text += "Tid: %5x   %s" % (threadInfo.tid, threadInfo.ip)

        self.setText(text)

        font = self.font()
        font.setBold(threadInfo.isCurrent)
        self.setFont(font)
        raise StopIteration

    def onDoubleClick(self):

        if self.kernel:
            yield ( self.uimanager.debugClient.callServerAsync(proclist.setCurrentCpu, self.targetId, self.tid ))
        else:
            yield ( self.uimanager.debugClient.callServerAsync(proclist.setCurrentThread, self.targetId, self.pid, self.tid))
        raise StopIteration
    
class ProcessItem(ThreadProcessItem):

    def __init__(self, processInfo, uimanager):
        super(ProcessItem,self).__init__(uimanager, "Pid: %x (%s)" % (processInfo.pid, processInfo.exeName) )
        self.pid = processInfo.pid
        self.threadRoot = ThreadRootItem(processInfo, self.uimanager)
        self.appendRow(self.threadRoot)
        self.setEditable(False)

    def update(self, processInfo):

        yield(self.uimanager.debugClient.callFunctionAsync(self.threadRoot.update, processInfo) )

        yield( self.uimanager.debugClient.callServerAsync(proclist.getTargetsList) )

        raise StopIteration


class ThreadRootItem(ThreadProcessItem):

    def __init__(self, processInfo, uimanager, kernel = False):
        super(ThreadRootItem,self).__init__(uimanager)
        self.kernel = kernel
        self.setEditable(False)

    def getThreadItem(self, threadInfo, row):
        threadItem = self.child(row) 
        if threadItem and threadItem.tid == threadInfo.tid:
            return threadItem
        return None

    def update(self, processInfo):

        try:
            threadList = yield(self.uimanager.debugClient.callServerAsync(proclist.getThreadList, processInfo.targetId, processInfo.pid))
            currentRow = 0
            for thread in threadList:
                threadItem = self.getThreadItem(thread, currentRow)
                if not threadItem:
                    threadItem = ThreadItem(thread, self.uimanager)
                    self.insertRow(currentRow, [threadItem])
                yield( self.uimanager.debugClient.callFunctionAsync(threadItem.update, thread) )
                currentRow += 1

            self.setRowCount(currentRow)
            if self.kernel:
                self.setText("CPU Cores: %d" % currentRow)
            else:
                self.setText("Threads: %d" % currentRow)

        except:
            print "!!!EXCEPTION"
            print sys.exc_info()

        raise StopIteration


class ProcessRootItem(ThreadProcessItem):

    def __init__(self, targetId, uimanager):
        super(ProcessRootItem,self).__init__(uimanager, "Processes: 0")
        self.setEditable(False)

    def update(self, targetInfo):
        try:
            processList = yield(self.uimanager.debugClient.callServerAsync(proclist.getProcessList,targetInfo.id))

            currentRow = 0
            for process in processList:
                processItem = self.getProcessItem(process, currentRow)
                if not processItem:
                    processItem = ProcessItem(process, self.uimanager)
                    self.insertRow(currentRow, [processItem])
                yield( self.uimanager.debugClient.callFunctionAsync(processItem.update, process) )
                currentRow += 1

            self.setRowCount(currentRow)
            self.setText("Processes: %d" % currentRow)

        except:
            print "!!!EXCEPTION"
            print sys.exc_info()

        raise StopIteration

    def getProcessItem(self,processInfo, row):

        processItem = self.child(row)
        if processItem and processItem.pid == processInfo.pid:
            return processItem
        return None

class TargetItem(ThreadProcessItem):

    def __init__(self, targetInfo, uimanager):
        super(TargetItem,self).__init__(uimanager, targetInfo.desc)
        self.desc = targetInfo.desc
        self.processRoot = None
        self.threadRoot = None
        self.isKernelDebugging = targetInfo.isKernelDebugging
        self.isDumpAnalyzing = targetInfo.isDumpAnalyzing

    def update(self, targetInfo):

        try:
            if self.isKernelDebugging or self.isDumpAnalyzing:
                processList = yield(self.uimanager.debugClient.callServerAsync(proclist.getProcessList, targetInfo.id))
                if not self.threadRoot:
                    self.threadRoot = ThreadRootItem(processList[0], self.uimanager, self.isKernelDebugging)
                    self.appendRow(self.threadRoot)

                yield(self.uimanager.debugClient.callFunctionAsync(self.threadRoot.update, processList[0]) )

            else:
                if not self.processRoot:
                    self.processRoot = ProcessRootItem(targetInfo.id, self.uimanager)
                    self.appendRow(self.processRoot)

                yield(self.uimanager.debugClient.callFunctionAsync(self.processRoot.update, targetInfo) )

        except:
            print "!!!EXCEPTION"
            print sys.exc_info()

        raise StopIteration

class ProcessExplorerWidget(NativeDataViewWidget):

    def __init__(self, widgetSettings, uimanager):
        super(ProcessExplorerWidget,self).__init__(uimanager)
        self.uimanager = uimanager

        self.treeView = QTreeView()
        self.treeView.setHeaderHidden(True)

        self.treeModel = QStandardItemModel(0,1)
        self.treeView.setModel(self.treeModel)

        self.treeView.setSelectionMode(QTreeView.NoSelection)
        self.treeView.setAllColumnsShowFocus(False)
        self.treeView.doubleClicked.connect(self.onItemDblClick)

        self.setWidget(self.treeView)

        self.uimanager.mainwnd.addDockWidget(Qt.TopDockWidgetArea, self)

        self.updateMutex = UpdateMutex()

    def getTargetItem(self, targetInfo, row):
        targetItem = self.treeModel.item(row)
        if targetItem and targetItem.desc == targetInfo.desc:
            return targetItem
        return None
    
    def dataUnavailable(self):
        self.treeModel.clear()
       
    @async
    def dataUpdate(self):

        self.treeView.setUpdatesEnabled(False)

        yield( self.uimanager.debugClient.lockMutexAsync(self.updateMutex) )

        with AutoQMutex(self.updateMutex) as autoMutex:

            targetsList = yield( self.uimanager.debugClient.callServerAsync(proclist.getTargetsList) )

            currentRow = 0
            for target in targetsList:
                targetItem = self.getTargetItem(target, currentRow)
                if not targetItem:
                    targetItem = TargetItem(target, self.uimanager)
                    self.treeModel.insertRow(currentRow, [targetItem])
                yield( self.uimanager.debugClient.callFunctionAsync(targetItem.update, target) )
                currentRow += 1

            self.treeModel.setRowCount(currentRow)

        self.treeView.setUpdatesEnabled(True)

        raise StopIteration

    @async    
    def onItemDblClick(self, modelIndex):
        item = self.treeModel.itemFromIndex(modelIndex)
        yield (self.uimanager.debugClient.callFunctionAsync(item.onDoubleClick))
        raise StopIteration



