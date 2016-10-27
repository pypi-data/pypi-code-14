
import telnetlib
import logging_helper

__author__ = u'Oli Davis'
__copyright__ = u'Copyright (C) 2016 Oli Davis'

logging = logging_helper.setup_logging()


class TelnetObj(object):

    def __init__(self,
                 ip,
                 timeout=5):

        self.tn = None
        self.ip = ip

        logging.info(u"Connecting to " + ip + u"...")
        try:
            self.tn = telnetlib.Telnet(ip, timeout=timeout)
            self.tn.read_until("login: ")
            self.tn.write("root" + "\n")
            self.tn.read_until("# ")
            logging.info(u"Connected!")

        except:
            raise Exception(u"Unable to connect to " + ip)

    def send_command(self,
                     command):

        # run the command
        try:
            self.tn.write(command + "\n")

        except Exception:
            logging.error(u"Unable to send the command to device")
            return

        return self.tn.read_until("# ")

    def readline(self):
        return self.tn.read_until("\n")
