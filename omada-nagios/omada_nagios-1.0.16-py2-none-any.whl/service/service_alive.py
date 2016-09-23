#!/usr/bin/env python2.7

from nagios import BaseCheckCommand

from optparse import OptionParser
import os
import commands

class ServiceAliveCheckCommand(BaseCheckCommand):
    def __init__(self, **kwargs):
        # Exit early if prereqs are not installed
        self.prerequites_test()

        # Invoke parent class's constructor
        self.__class__.__bases__[0].__init__(self,\
                parser=OptionParser(usage='%prog [options] SERVICE_NAME', version="%prog 1.0"))

        # Constructor for CollectorLastMessage
        self.add_options()
        params      = kwargs
        opts, args  = self.parse_args()

        self.service_name   = params.get('service_name') or args[0]

        self.warning        = int(opts.warning)
        self.critical       = int(opts.critical)

    def add_options(self):
        pass

    def prerequites_test(self):
        pass

    def check(self):
        try:
            status_appendix, service_is_healthy = self.service_healthy()
            if service_is_healthy:
                self.status = "Service %s is running. Init unit reports: %s" % (self.service_name, status_appendix)
                self.exit(exit_code=0)
            else:
                self.status = "Service %s is NOT running. Init unit reports: %s" % (self.service_name, status_appendix)
                self.exit(exit_code=2)
        except Exception as e:
            self.status = e.message
            self.exit(exit_code=3)

    def service_healthy(self):
        init = self._find_init_type()

        if init == 'upstart':
            exit_code, out = commands.getstatusoutput('status %s' % self.service_name)
        elif init == 'sysv':
            exit_code, out = commands.getstatusoutput('service %s status' % self.service_name)
        else:
            raise Exception("Unable to determine service health for %s" % self.service_name)

        if exit_code != 0:
            return (out.replace('\n', ''),False)
        else:
            return (out.replace('\n', ''),True)

    def _find_init_type(self):
        if os.path.exists('/etc/init/%s' % self.service_name):
            return 'upstart'

        if os.path.exists('/etc/init.d/%s' % self.service_name):
            return 'sysv'

        return None
