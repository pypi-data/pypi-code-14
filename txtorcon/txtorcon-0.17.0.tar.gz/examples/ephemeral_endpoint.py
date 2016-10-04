from __future__ import print_function

# This connects to the system Tor (by default on control port 9151)
# and adds a new hidden service configuration to it.

from twisted.internet import defer
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.web import server, resource
from twisted.internet.task import react

import txtorcon
from txtorcon.util import default_control_port


# Ephemeral endpoints. You own all the bits.
securely_stored_keyblob = '''RSA1024:MIICWwIBAAKBgQCsEuaUlvU651/lEl986XfX4QylkQCLhA9Nc19LTTt38oDeHRl3i5VgNsfsXyLrnk2iWapOsc3nmvxMt9vhFFanDB9p/rZTonERnTAw50M7PP4H4E8MDkPm6yZJSES7TPEI9u7WfSdq/HsNk4bsQU9Q3Vndy+hPZtPeGl+rs+3MawIDAQABAoGAGHPDIoBlLs6sWOAIg7almh7X7jsxyaGljwsDEq9R8RSb7XRTJyLFwltmg5dtXfAr9hMp2W745J2olrpV26FJQs4LFQBFawUwytvSV9IanpOew02yjvUQ0zqQUUbuR8rNHhzxJrvfJLDEzCmB8RBb1fE6BcUdv5t8xCu0/BwJdCkCQQDaL1ZJQ4aVHLcqru3IqiAwLsnA62aMNUPOO7twJ4YArX7Q6ZscqOPp8eLLoRzCYpMODcBX7kAOmuHxW8X3AKqnAkEAyeWoW01hlTzSY9kY/rMJOx5GKgDq3yqjyhshbEL1HDBh7mdt+4hTV2+a0L8CNCivfI7bbAS0oFCGRtX/Kgo8nQJBAIsxe+jNjYR/h1NRuh00e8iBcPEEvK1iJdniPZg1fsXb6XW6Mty72nsbd8bVCBXy8UIb/8OZGYC3ysFB/S+xWy0CQGHHtC3j4Cri9hIdhpl0JDhZhSm6oAXNJN4xHZLNKuCoHgXUWdPERnjGOHh4yZxxR+xPU72Q2dn6pc2Qvq+hnZECPzZ4O79cP7Y1ungZSzLZnoh0h1P9pSKDOq8qyyBD7SgW3tDGg04vkprlYnMH5EKp+BLC6rk4KRx0Za3wrY6Thw=='''


class Simple(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        return "<html>Hello, world! I'm a hidden service!</html>"


@defer.inlineCallbacks
def main(reactor):
    ep = txtorcon.TCPHiddenServiceEndpoint.system_tor(
        reactor,
        public_port=8080,
        control_endpoint=TCP4ClientEndpoint(reactor, 'localhost', default_control_port()),
        private_key=securely_stored_keyblob,
        ephemeral=True
    )

    def on_progress(percent, tag, msg):
        print('{:3.0f}%: {}'.format(percent, msg))
    txtorcon.IProgressProvider(ep).add_progress_listener(on_progress)

    print("Starting site")
    port = yield ep.listen(server.Site(Simple()))
    host = port.getHost()

    print("Site started. Available at http://{}:{}".format(host.onion_uri, host.onion_port))
    print("Private key:\n{}".format(host.onion_key))

    # if you have need of the actual IOnionService object (e.g. an
    # EphemeralHiddenService or FilesystemHiddenService instance) then
    # you can get it via the port (which itself is a
    # TorOnionListeningPort instance)
    service = port.onion_service

    print("Ports:", service.ports)
    print("Hostname:", service.hostname)
    print("Private key:", service.private_key)

    # wait forever; obviously you could do other work here
    d = defer.Deferred()
    yield d


if __name__ == '__main__':
    react(main)
