import time
from concurrent.futures import *
from subprocess import *


def make_call():
    print 'go'
    return_code = check_call(r'dir C:\Windows\System32', shell=True, stdout=PIPE)
    # output = process.communicate()[0]
    output = return_code
    print output
    time.sleep(3)
    return output


with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(make_call) for i in xrange(3)]
    wait(futures)

print 'DONE'
