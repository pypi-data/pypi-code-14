import fcntl, multiprocessing, time

f = open('l', 'w')
fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)

try:
    fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
except IOError:
    pass # shouldn't be able to lock

p = multiprocessing.Process(target=time.sleep, args=(3,))
p.daemon = True
p.start()

fcntl.flock(f.fileno(), fcntl.LOCK_UN)
f.close()

f = open('l', 'a+')
try:
    fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
except IOError:
    print('Failed to get lock, why?')
    p.join()

    # The process stopped, now we can get the lock
    fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
else:
    print('Yay, we got yhe lock!')

