from PyPPM import ppmGenerator
import time

print "hello world"
g = ppmGenerator()
g.start()
for asdf in range(0,10):
    g.set_channel_values([2,1,2,1,2,1,2,1])
    time.sleep(1)
    g.set_channel_values([1,2,1,2,1,2,1,2])
    time.sleep(1)
g.stop()