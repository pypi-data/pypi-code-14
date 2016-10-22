import OSC
import threading
import time

class MuseMock(threading.Thread):
    def __init__(self, sample_rate, data_src, server_addr):
        super(MuseMock, self).__init__()
        self.sample_rate = sample_rate
        self.data_src = data_src
        self.sleep_time = 1 / sample_rate
        self.server_addr = server_addr
        self.osc_client = MyOSCClient()
        self.run_flag = False
        self.connected = False

    def connect(self):
        self.osc_client.connect(self.server_addr)
        self.connected = True

    def transmit(self):
        if not self.connected:
            self.connect()

        with open(self.data_src, mode='rt') as f:
            try:
                line = f.readline().split(',')
                del line[-1]
                counter = 1
                while self.run_flag and line:
                    msg = OSC.OSCMessage(line.pop(0))
                    msg.append(line)
                    self.osc_client.send(msg)
                    time.sleep(self.sleep_time)
                    line = f.readline().split(',')
                    del line[-1]
                    counter += 1
            except IOError as e:
                print 'exception in testlib'
                print e.message

            print 'file counter - ' + str(counter)

        print 'End of transmission'

    def run(self):
        print 'MuseMock Started'
        self.transmit()


class MyOSCClient(OSC.OSCClient):
    # set outgoing socket buffer size
    sndbuf_size = 4096 * 32

    def __init__(self, server=None):
        super(MyOSCClient, self).__init__(server)
