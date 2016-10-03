__author__ = 'marcoantonioalberoalbero'

import multiprocessing


class Threads:
    def __init__(self):
        pass

    @staticmethod
    def run_detached(routine):
        p = multiprocessing.current_process()
        name = "worker-" + str(p.pid)
        cc = multiprocessing.Process(name=name, target=routine)
        cc.daemon = False
        cc.start()