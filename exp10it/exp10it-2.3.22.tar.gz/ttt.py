import threading
import time
import sys
import readline
'''
class MyThread(threading.Thread):
    def __init__(self,func,args,name=''):
        threading.Thread.__init__(self)
        self.name=name
        self.func=func
        self.args=args
    def run(self):
        self.result=apply(self.func,self.args)
    def get_result():
        return self.result

def get_input_intime(default_choose,timeout=5):
    default_choose=[default_choose]
    timeout=[timeout]
    choosed=[0]
    chioce=['']
    def print_time_func():
        while choosed[0]==0 and timeout[0]>0:
            time.sleep(1)
            sys.stdout.write('\r'+' '*(len(readline.get_line_buffer())+2)+'\r')
            print "%s seconds left...please input your chioce:>" % timeout[0]
            sys.stdout.write('> ' + readline.get_line_buffer())
            sys.stdout.flush()
            timeout[0]-=1
        if choosed[0]==0:
            chioce[0]=default_choose[0]
    def input_func():
        while choosed[0]==0 and timeout[0]>0:
            s = raw_input('> ')
            #rlist, _, _ = select([sys.stdin], [], [], timeout[0])

            if len(s)==0:
                chioce[0]=default_choose[0]
                choosed[0]=1
                print "you choosed the default chioce:%s" % default_choose[0]
            else:
                chioce[0]=s
                choosed[0]=1
                print "you choosed %s" % chioce[0]

    time_left_thread=MyThread(print_time_func,())
    input_thread=MyThread(input_func,())
    time_left_thread.start()
    #input_thread.setDaemon(True)
    input_thread.start()
    time_left_thread.join()
    if choosed[0]==0:
        print "i choose the default chioce for you:%s" % chioce[0]
    return chioce[0]
get_input_intime('targets.txt',20)
'''
from exp10it import *
get_input_intime('targets.txt',20)
