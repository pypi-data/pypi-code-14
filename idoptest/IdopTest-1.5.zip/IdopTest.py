import logging , sys , time, datetime , os , threading

ver = "1.5"
print "IdopTest Imported " + ver

def getVersion():
    print "IdopTest get Version " + ver

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

def initLog():
    logging.basicConfig(filename='IdoTest.log',level=logging.INFO , format='%(asctime)s %(message)s')    
    logging.info('===============================')
    logging.info('IdoTest Init')

def ci_print(msg , level = ''):
    try:
        msg = ver + ' '  + msg
        if level=='info':
            logging.info(msg)
        else:
            logging.warning(msg)
            
        print msg
    except Exception as inst:
        logging.warning('Main Exception :: ' + inst)

def MainLoop():
    try:    
        ci_print('Loop run at ' + str(datetime.datetime.now()))
    except Exception as inst:
        print "Error MainLoop " + str(inst)        
        logging.warning('Error in MainLoop :: ' + str(inst))

    #ci_print('===============================')
    #ci_print('CI_LocalConnector Ended')
    
def MainLoopStart():
    try:
        ci_print("IdopTest Started")
        rt = RepeatedTimer(5, MainLoop)
    except Exception as inst:
        ci_print("Error MainLoopStart " + str(inst))

initLog()
if (len(sys.argv)>1 and sys.argv[1]=='MainLoopStart'):
    MainLoopStart()
if (len(sys.argv)>1 and sys.argv[1]=='MainLoop'):
    MainLoop()


