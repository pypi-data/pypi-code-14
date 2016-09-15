# -*- coding: utf-8 -*-
import threadpool
import Queue
import  time
import random
from threading import  current_thread

class Demo:
    def __init__(self):
        self.q = Queue.Queue()
        self.running = True

    def f1(self,queue):
        cnt = 0
        while self.running:
            time.sleep(random.randint(0, 2))
            queue.put(cnt)
            cnt += 1
            if cnt == 20:
                queue.put(-1)
                break

    def f2(self,queue):
        while self.running:
            time.sleep(random.randint(0, 3))
            try:
                data = queue.get(True,2)
                if data is not None:
                    if data == -1:
                        print "Found quit flag"
                        queue.put(data)
                        break
                    print "[%s] consumer pick %d" % (current_thread().name, int(data))
            except Exception,e: pass

    def run(self):
        pool = threadpool.ThreadPool(3)

        requests = threadpool.makeRequests(self.f1,(self.q,))
        [pool.putRequest(req) for req in requests]

        requests = threadpool.makeRequests(self.f2,(self.q,self.q,self.q))
        [pool.putRequest(req) for req in requests]
        pool.wait()

if __name__ == '__main__':
    d = Demo()
    d.run()