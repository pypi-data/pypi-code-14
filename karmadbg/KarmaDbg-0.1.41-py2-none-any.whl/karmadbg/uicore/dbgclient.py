import time
import os.path
import cgi
import re

from threading import Lock

from PySide.QtCore import QObject, QThreadPool, QRunnable, Signal, QMutex, QWaitCondition

from karmadbg.dbgcore.dbgengine import DbgEngine, LocalDebugServer
from karmadbg.uicore.async import AsyncOperation, async

class DebugAsyncCall(QObject, QRunnable):

    asyncDone = Signal(object)

    def __init__(self, dbgclient):
        QObject.__init__(self)
        QRunnable.__init__(self)
        self.dbgclient = dbgclient
        self.asyncmgr = dbgclient.asyncMgr
  
    def doTaskAsync(self):
        self.asyncmgr.start(self)

    def run(self):

        try:
            res = self.task()
        except Exception, ex:
            res = ex

        self.asyncDone.emit((res,))

        if self.dbgclient.currentThreadChanged:
            self.dbgclient.currentThreadChanged = False
            self.dbgclient.targetThreadChanged.emit()

        if self.dbgclient.currentFrameChanged:
            self.dbgclient.currentFrameChanged = False
            self.dbgclient.targetFrameChanged.emit()

    def task(self):
        pass

class AsyncProfiler(object):

    def __init__(self, dbgClient, str):
        self.dbgClient = dbgClient
        self.dbgClient.uimanager.debugOutput(str)

    def __enter__(self):
        self.startTime = time.time()*1000

    def __exit__(self, type, value, traceback):
        self.dbgClient.uimanager.debugOutput( "complete. took time = %dms" % ( time.time()*1000 - self.startTime ) )


class DebugClient(QObject):

    outputPlainReady = Signal()
    outputFormattedReady = Signal()

    targetRunning = Signal()
    targetStopped = Signal()
    targetDetached = Signal()
    targetThreadChanged = Signal()
    targetFrameChanged = Signal()
    targetBreakpointsChanged = Signal()
    tagetSymbolPathsChanged = Signal()

    pythonStarted = Signal(str)
    pythonRunning = Signal()
    pythonStopped = Signal()
    pythonExit = Signal()
    pythonDataChanged = Signal()
    pythonBreakpointAdded = Signal(str,int)
    pythonBreakpointRemoved = Signal(str,int)
    pythonStackFrameChanged = Signal()

    def __init__(self, uimanager, dbgsettings):

        super(DebugClient,self).__init__()
        self.uimanager = uimanager

        self.activePythonDbg = False

        self.dbgServer = LocalDebugServer()
        self.dbgEngine = DbgEngine(self, self.dbgServer, dbgsettings)

        self.asyncMgr = QThreadPool()
        self.asyncMgr.setMaxThreadCount(1)

        self.waitPool = QThreadPool()

        self.currentFrameChanged = False
        self.currentThreadChanged = False

        self._stepSourceMode = False

        self.outputMutex = Lock()
        self.outputPlain = ""
        self.outputFormatted = ""

    def start(self):
        self.dbgEngine.start()
        self.serverControl = self.dbgServer.getServerControl()
        self.serverInterrupt = self.dbgServer.getServerInterrupt()
        #

    def stop(self):
        self.dbgEngine.stop()
        self.asyncMgr.waitForDone()

    def getPlainOutput(self):
        self.outputMutex.acquire()
        l = self.outputPlain 
        self.outputPlain = ""
        self.outputMutex.release()
        return l

    def getFormattedOutput(self):
        self.outputMutex.acquire()
        l = self.outputFormatted
        self.outputFormatted = ""
        self.outputMutex.release()
        return l

### debug client callbacks ###

    def quit(self):
        self.uimanager.quit()

    def output(self, str, dml):

        self.outputMutex.acquire()

        if self.outputPlain == "":
            self.outputPlainReady.emit()

        self.outputPlain += str

        if self.outputFormatted == "":
            self.outputFormattedReady.emit()

        if not dml:
            str = cgi.escape(str)
       
        str = re.sub(r"<link cmd", "<a href", str)
        str = re.sub("</link>", "</a>", str)
        str = re.sub("<exec cmd", "<a href", str)
        str = re.sub("</exec>", "</a>", str)

        #str = str.replace(" ", "&nbsp;")
        #str = str.replace("\t", "&nbsp;"*4)
        #str = str.replace("\r", "")
        #str = str.replace("\n", "<br>")

        self.outputFormatted += str

        self.outputMutex.release()

    def input(self):
        return self.uimanager.textInput()


###  native debugger state callbacks ###

    def onTargetStateChanged(self,state):
        if state.IsRunning:
            self.targetRunning.emit()
        elif state.IsStopped:
            self.targetStopped.emit()
        elif state.IsNoTarget:
            self.targetDetached.emit()

    def onTargetChangeCurrentThread(self):
        self.currentThreadChanged = True

    def onTargetChangeCurrentFrame(self, frame):
        self.currentFrameChanged = True

    def onTargetChangeBreakpoints(self):
        self.targetBreakpointsChanged.emit()

    def onChangeSymbolPaths(self):
        self.tagetSymbolPathsChanged.emit()

### python debugger state callbacks

    def onPythonStart(self, scriptPath):
        self.activePythonDbg = True
        self.pythonStarted.emit(scriptPath)
        return True

    def onPythonQuit(self):
        self.pythonExit.emit()
        self.activePythonDbg = False

    def onPythonStateChanged(self,state):
        if state.IsRunning:
            self.pythonRunning.emit()
        elif state.IsStopped:
            self.pythonStopped.emit()

    def onPythonStackFrameChanged(self, frameno):
        self.pythonStackFrameChanged.emit()

    def onPythonBreakpointAdd(self, filename, lineno):
        self.pythonBreakpointAdded.emit(filename, lineno)

    def onPythonBreakpointRemove(self, filename, lineno):
        self.pythonBreakpointRemoved.emit(filename, lineno)


### debug engine interrupts ###
        
    def breakin(self):
        self.serverInterrupt.breakin()
        
### debug engine async API ###

    def callServerCommandAsync(self, commandStr):

        class CallServerCommandAsync(DebugAsyncCall):

          def task(self):
                with AsyncProfiler(self.dbgclient, "call command \"%s\"" % commandStr ) as profiler:
                    return self.dbgclient.serverControl.debugCommand(commandStr)
    
        return CallServerCommandAsync(self)


    def callServerAsync(self, func, *args, **kwargs):

        class CallServerAsync(DebugAsyncCall):

            def task(self):
                with AsyncProfiler(self.dbgclient, "call server async: %s" % str(func) ) as profiler:
                    return self.dbgclient.serverControl.callFunction( func, *args, **kwargs)
    
        return CallServerAsync(self)

    @async
    def callServer(self, func, *args, **kwargs):
        yield( self.callServerAsync(func, *args, **kwargs))


    def lockMutexAsync(dbgclient,mutex):

        class LockMutexAsync(QObject, QRunnable):

            asyncDone = Signal(object)

            def __init__(self):
                QObject.__init__(self)
                QRunnable.__init__(self)

            def doTaskAsync(self):
                dbgclient.waitPool.start(self)

            def run(self):
                mutex.lock()
                self.asyncDone.emit((None,))

        return LockMutexAsync()


    def callFunctionAsync(self, fn, *args, **kwargs):

        class CallFunctionAsync(QObject):

            asyncDone = Signal(object)

            def __init__(self):
                QObject.__init__(self)

            def doTaskAsync(self):
                try:
                    self.async = fn(*args, **kwargs)
                    self.asyncOp = self.async.next()
                    self.asyncOp.asyncDone.connect(self.onAsyncDone)
                    self.asyncOp.doTaskAsync()
                except StopIteration:
                    self.asyncDone.emit((None,))

            def onAsyncDone(self, result):
                try:
                    if isinstance(result[0], Exception):
                        self.asyncOp = self.async.throw(result[0])
                    else:
                        self.asyncOp = self.async.send(result[0])
                    self.asyncOp.asyncDone.connect(self.onAsyncDone)
                    self.asyncOp.doTaskAsync()
                except StopIteration:
                    self.asyncDone.emit((None,))

        return CallFunctionAsync()


    def getAutoCompleteAsync(self, startCompleteStr):

        class AutoCompleteAsync(DebugAsyncCall):

            def task(self):
                with AsyncProfiler(self.dbgclient, "get auto complete for \"%s\"" % startCompleteStr ) as profiler:
                    return self.dbgclient.serverControl.getAutoComplete(startCompleteStr)

        return AutoCompleteAsync(self)


# native debugger async API


    def getSourceLineAsync(self, addr=0):

        class SourceLineAsync(DebugAsyncCall):

            def task(self):
                with AsyncProfiler(self.dbgclient, "get source line") as profiler:
                    return self.dbgclient.serverControl.getSourceLine(addr)

        return SourceLineAsync(self)


    def getSourceFileFromServerAsync(self, addr=0):

        class SourceLineFromServerAsync(DebugAsyncCall):

            def task(self):
                with AsyncProfiler(self.dbgclient, "get source file from source server") as profiler:
                    return self.dbgclient.serverControl.getSourceFromServer(addr)

        return SourceLineFromServerAsync(self)


    def getDisasmAsync(self, relpos, linecount):

        class DisasmAsync(DebugAsyncCall):

            def task(self):
                with AsyncProfiler(self.dbgclient, "get disasm relpos = %d linecount = %d" % (relpos, lienpos) ) as profiler:
                    return self.dbgclient.serverControl.getDisasm(relpos, linecount)

        return DisasmAsync(self)


    def getRegistersAsync(self):

        class RegisterAsync(DebugAsyncCall):

            def task(self):
                with AsyncProfiler(self.dbgclient, "get register") as profiler:
                    return self.dbgclient.serverControl.getRegsiters()
    
        return RegisterAsync(self)


    def getStackTraceAsync(self):

        class StackTraceAsync(DebugAsyncCall):

            def task(self):
                with AsyncProfiler(self.dbgclient, "get stack") as profiler:
                    return self.dbgclient.serverControl.getStackTrace()

        return StackTraceAsync(self)

    def setCurrentFrameAsync(self, frameno):

        class CurrentFrameAsync(DebugAsyncCall):

            def task(self):
                with AsyncProfiler(self.dbgclient, "set current frame no = %d" % frameno) as profiler:
                    return self.dbgclient.serverControl.setCurrentFrame(frameno)

        return CurrentFrameAsync(self)

    @async
    def setCurrentFrame(self, frameno):
        ret = yield( self.setCurrentFrameAsync(frameno))
        assert( ret == None)

    def getCurrentFrameAsync(self):

        class CurrentFrameAsync(DebugAsyncCall):

            def task(self):
                with AsyncProfiler(self.dbgclient, "get current frame") as profiler:
                    return self.dbgclient.serverControl.getCurrentFrame()

        return CurrentFrameAsync(self)

    def getExpressionAsync(self, expr):

        class ExpressionAsync(DebugAsyncCall):

            def task(self):
                with AsyncProfiler(self.dbgclient, "get expression \"%s\"" % expr) as profiler:
                    return self.dbgclient.serverControl.getExpr(expr)

        return ExpressionAsync(self)

    def getMemoryAsync(self, expression="", offset=0, length = 0x10):

        class MemoryAsync(DebugAsyncCall):

            def task(self):
                with AsyncProfiler(self.dbgclient, "read memory expession=%s offset=%x len=%d" % (expression, offset, length)) as profiler:
                    return self.dbgclient.serverControl.getMemory(expression,offset,length)

        return MemoryAsync(self)


    def pythonEvalAsync(self, expr):

        class PythonEvalAsync(DebugAsyncCall):

            def task(self):
                with AsyncProfiler(self.dbgclient, "python eval \"%s\"" % expr ) as profiler:
                    return self.dbgclient.serverControl.pythonEval(expr)

        return PythonEvalAsync(self)

    def getLiveProcessListAsync(self):

        class LiveProcessList(DebugAsyncCall):

            def task(self):
                with AsyncProfiler(self.dbgclient, "get system process list") as profiler:
                    return self.dbgclient.serverControl.getLiveProcessList()

        return LiveProcessList(self)

    @property
    def stepSourceMode(self):
        return self._stepSourceMode

    @stepSourceMode.setter
    def stepSourceMode(self, val):
        self.setStepSourceMode(val)
 
    @async
    def setStepSourceMode(self, val):

        self._stepSourceMode = val == True

        class setStepSourceModeAsync(DebugAsyncCall):

            def task(self):
                with AsyncProfiler(self.dbgclient, "set source step mode" ) as profiler:
                    self.dbgclient.serverControl.setStepSourceMode(val)

        yield( setStepSourceModeAsync(self) )


    def addBreakpointAsync(self,filename,lineno):

        class AddBreakpointAsync(DebugAsyncCall):
            def task(self):
                with AsyncProfiler(self.dbgclient, "add breakpoint filename=%s lineno=%d" % (filename,lineno) ) as profiler:
                    return self.dbgclient.serverControl.addBreakpoint(filename,lineno)
        
        return AddBreakpointAsync(self)


    @async
    def addBreakpoint(self,filename,lineno):
        yield ( self.addBreakpointAsync(filename, lineno) )


    def removeBreakpointAsync(self,filename,lineno):

        class RemoveBreakpointAsync(DebugAsyncCall):
            def task(self):
                with AsyncProfiler(self.dbgclient, "remove breakpoint filename=%s lineno=%d" % (filename,lineno) ) as profiler:
                    return self.dbgclient.serverControl.removeBreakpoint(filename,lineno)

        return RemoveBreakpointAsync(self)

    @async
    def removeBreakpoint(self, filename,lineno):
        yield ( self.removeBreakpointAsync(filename,lineno) )

    def getPromptAsync(self):

        class PromptAsync(DebugAsyncCall):
            def task(self):
                with AsyncProfiler(self.dbgclient, "get prompt" ) as profiler:
                    return self.dbgclient.serverControl.getPrompt()

        return PromptAsync(self)

### extended command
    def openSourceCmd(self, args):

        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("filename", nargs='?')
        parser.add_argument("-a", type=str)

        args  = parser.parse_args(args)

        fileName = ""
        line = 0

        if args.filename:
            fileName = args.filename
        
        else:

            addr = 0

            if args.a:
                addr = self.serverControl.getExpr(args.a)
                if not addr:
                    return

            fileName, line = self.serverControl.getSourceLine(addr)
            if not fileName:
               return

            if not os.path.exists(fileName):
                fileName = self.serverControl.getSourceFromServer(addr)

            if fileName == "":
                return

        self.uimanager.showSourceFile(fileName, line)


### Python debugger async API  ### 

    def getPythonSourceLineAsync(self):

        class PythonSourceLineAsync(DebugAsyncCall):

            def task(self):
                with AsyncProfiler(self.dbgclient, "get python source line") as profiler:
                    return self.dbgclient.serverControl.getPythonSourceLine()

        return PythonSourceLineAsync(self)

    def getPythonStackTraceAsync(self):

        class PythonStackTraceAsync(DebugAsyncCall):

            def task(self):
                with AsyncProfiler(self.dbgclient, "get python stack trace") as profiler:
                    return self.dbgclient.serverControl.getPythonStackTrace()

        return PythonStackTraceAsync(self)

    def getPythonBreakpointListAsync(self):

        class PythonBreakpointListAsync(DebugAsyncCall):

            def task(self):
                with AsyncProfiler(self.dbgclient, "get python breakpoints") as profiler:
                    return self.dbgclient.serverControl.getPythonBreakpointList()

        return PythonBreakpointListAsync(self)

    def getPythonLocalsAsync(self, localsName):

        class PythonLocalsAsync(DebugAsyncCall):

            def task(self):
                with AsyncProfiler(self.dbgclient, "get python locals") as profiler:
                    return self.dbgclient.serverControl.getPythonLocals(localsName)

        return PythonLocalsAsync(self)


    def addPythonBreakpointAsync(self,filename,lineno):

        class AddPythonBreakpointAsync(DebugAsyncCall):
            def task(self):
                with AsyncProfiler(self.dbgclient, "add python breakpoint filename=%s lineno=%d" % (filename,lineno) ) as profiler:
                    return self.dbgclient.serverControl.setPythonBreakpoint(filename,lineno)
        
        return AddPythonBreakpointAsync(self)


    @async
    def addPythonBreakpoint(self,filename,lineno):
        yield ( self.addPythonBreakpointAsync(filename, lineno) )


    def removePythonBreakpointAsync(self,filename,lineno):

        class RemovePythonBreakpointAsync(DebugAsyncCall):
            def task(self):
                with AsyncProfiler(self.dbgclient, "remove  python breakpoint filename=%s lineno=%d" % (filename,lineno) ) as profiler:
                    return self.dbgclient.serverControl.removePythonBreakpoint(filename,lineno)

        return RemovePythonBreakpointAsync(self)

    @async
    def removePythonBreakpoint(self, filename,lineno):
        yield ( self.removePythonBreakpointAsync(filename,lineno) )


    def setPythonCurrentFrameAsync(self, frameno):

        class SetPythonCurrentFrameAsync(DebugAsyncCall):

            def task(self):
                with AsyncProfiler(self.dbgclient, "set current frame no = %d" % frameno) as profiler:
                    return self.dbgclient.serverControl.setPythonCurrentFrame(frameno)

        return SetPythonCurrentFrameAsync(self)

    @async
    def setPythonCurrentFrame(self, frameno):
        ret = yield( self.setPythonCurrentFrameAsync(frameno))
        assert( ret == None)

    def getPythonCurrentFrameAsync(self):

        class GetPythonCurrentFrameAsync(DebugAsyncCall):

            def task(self):
                with AsyncProfiler(self.dbgclient, "get current frame") as profiler:
                    return self.dbgclient.serverControl.getPythonCurrentFrame()

        return GetPythonCurrentFrameAsync(self)

