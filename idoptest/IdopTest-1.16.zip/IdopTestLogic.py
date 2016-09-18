import logging , sys , time, datetime , os , threading

ver = "1.16"
print "IdopTestLogic Imported " + ver

def getVersion():
    print "IdopTest get Version " + ver

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



