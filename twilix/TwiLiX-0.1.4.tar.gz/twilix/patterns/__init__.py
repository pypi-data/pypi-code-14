from twisted.internet import task

from twilix.jid import internJID

class BasePattern(object):
    def __init__(self, myjid, keepalive_period=None):
        """
        :param myjid: The jid of the component.
        :param keepalive_period: The number of seconds between sending
        of keepalives.
        """
        self.myjid = internJID(myjid)
        self.keepalive_period = keepalive_period
        self.keepalive_send_task = task.LoopingCall(self.send_keepalive)

    def send_keepalive(self):
        self.xmlstream.transport.write(' ')

    def startSendingKeepalives(self):
        if self.keepalive_period:
            self.keepalive_send_task.start(self.keepalive_period)

    def stopSendingKeepalives(self):
        if self.keepalive_period:
            self.keepalive_send_task.stop()
