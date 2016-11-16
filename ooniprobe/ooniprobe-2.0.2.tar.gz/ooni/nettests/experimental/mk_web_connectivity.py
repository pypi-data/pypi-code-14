from ooni.templates import mk
from ooni.utils import log
# from twisted.internet import defer, protocol, reactor
from twisted.python import usage


class UsageOptions(usage.Options):
    optParameters = []


class MKWebConnectivity(mk.MKTest):
    name = "Web Connectivity"
    version = "0.1.0"

    usageOptions = UsageOptions
    requiresRoot = False
    requiresTor = False

    def test_run(self):
        log.msg("Running web connectivity on %s" % self.input)
        options = {
            'foo': 'bar'
        }
        return self.run("WebConnectivity", options, self.input)
