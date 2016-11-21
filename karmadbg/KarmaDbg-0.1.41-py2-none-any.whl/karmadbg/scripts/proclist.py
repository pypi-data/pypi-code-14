import pykd

class ThreadInfo(object):

    def __init__(self, targetId, pid, thread):
        self.targetId = targetId
        self.pid = pid
        self.tid = thread.systemID
        self.isCurrent = thread.isCurrent()
        self.isKernel =  False
        ip = thread.ip
        try:
            module = pykd.targetSystem.getSystemById(targetId).getProcessBySystemId(pid).getModuleByOffset(ip)
            self.ip = "%s!%s" % ( module.name(), module.findSymbol(ip) )
        except pykd.DbgException:
            self.ip = str(thread.ip)


class KernelThreadInfo(object):

    def __init__(self, targetId, cpu, thread):
        self.targetId = targetId
        self.pid = 0
        self.tid = cpu
        self.isCurrent = thread.isCurrent()
        self.isKernel = True
        ip = thread.ip
        try:
            module = pykd.targetSystem.getSystemById(targetId).getProcess(0).getModuleByOffset(ip)
            self.ip = "%s!%s" % ( module.name(), module.findSymbol(ip) )
        except pykd.DbgException:
            self.ip = str(thread.ip)

class ProcessInfo(object):

    def __init__(self, targetId, process):
        self.exeName = process.exeName
        self.pid = process.systemID
        self.id = process.id
        self.targetId = targetId
        self.isCurrent = process.isCurrent()

class KernelProcessInfo(object):

    def __init__(self, targetId, process):
        self.exeName = process.exeName
        self.pid = 0
        self.id = process.id
        self.targetId = targetId
        self.isCurrent = True

class TargetInfo(object):

    def __init__(self, target):
        self.desc = target.desc
        self.id = target.id
        self.isCurrent = target.isCurrent()
        self.isKernelDebugging = target.isKernelDebugging()
        self.isDumpAnalyzing = target.isDumpAnalyzing()

def getThreadList(targetId, pid):
     targetSystem = pykd.targetSystem.getSystemById(targetId)
     if targetSystem.isKernelDebugging():
        targetProcess = targetSystem.getProcess(0)
        return [KernelThreadInfo(targetId, i, targetProcess.getThread(i) ) for i in xrange(targetProcess.getNumberThreads())]
     else:
        targetProcess = targetSystem.getProcessBySystemId(pid)
        return [ThreadInfo(targetId, pid, targetProcess.getThread(i)) for i in xrange(targetProcess.getNumberThreads())]

def getProcessList(targetId):
    targetSystem = pykd.targetSystem.getSystemById(targetId)
    if targetSystem.isKernelDebugging():
        return [KernelProcessInfo(targetId, targetSystem.getProcess(i))  for i in xrange(targetSystem.getNumberProcesses()) ]
    else:
        return [ProcessInfo(targetId, targetSystem.getProcess(i)) for i in xrange(targetSystem.getNumberProcesses()) ]

def getTargetsList():
    return [ TargetInfo(pykd.targetSystem(i)) for i in xrange( pykd.targetSystem.getNumber()) ]

def setCurrentThread(targetId, pid, tid):
    pykd.targetSystem.getSystemById(targetId).getProcessBySystemId(pid).getThreadBySystemId(tid).setCurrent()

def setCurrentCpu(targetId, cpu):
    pykd.targetSystem.getSystemById(targetId).getProcess(0).getThreadById(cpu).setCurrent()
