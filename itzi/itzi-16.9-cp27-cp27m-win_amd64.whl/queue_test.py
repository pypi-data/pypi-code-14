from multiprocessing import Process, Queue

def f(q):
    q.put([42, None, 'hello'])

if __name__ == '__main__':
    q = Queue()
    for i in range(5):
        p = Process(target=f, args=(q,))
        p.start()
        print q.get()    # prints "[42, None, 'hello']"
        p.join()
