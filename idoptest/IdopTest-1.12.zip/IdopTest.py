import logging , sys , time, datetime , os , threading , IdopTestLogic ,pip

print "IdopTest Main Imported "

from threading import Timer
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

def MainLoop():
    try:
		#IdopTest.ci_print('222')
		reload(IdopTestLogic)
		pip.main(['install','IdopTest'])
		#IdopTest.ci_print('222')	
		IdopTestLogic.ci_print('Loop run at ' + str(datetime.datetime.now()))
    except Exception as inst:
        print "Error MainLoop " + str(inst)        
        logging.warning('Error in MainLoop :: ' + str(inst))

    #ci_print('===============================')
    #ci_print('IdopTest Ended')
   
def MainLoopStart():
    try:
        IdopTestLogic.ci_print("IdopTest Started")
        rt = RepeatedTimer(5, MainLoop)
    except Exception as inst:
        IdopTestLogic.ci_print("Error MainLoopStart " + str(inst))

IdopTestLogic.initLog()
if (len(sys.argv)>1 and sys.argv[1]=='MainLoopStart'):
    MainLoopStart()
if (len(sys.argv)>1 and sys.argv[1]=='MainLoop'):
    MainLoop()


