import socket
import struct
import sys
from optparse import OptionParser
from select import select
import logging

def get_option_parser():
    parser = OptionParser()

    parser.add_option("-p", "--ports", dest="ports", default="8773",
                      help="Comma separated list of Source Ports to filter on", metavar='PORT')

    parser.add_option("-t", "--timeout", dest="timeout", type="int", default=None,
                      help="Amount of time to collect packets'",
                      metavar='COUNT')

    parser.add_option("-c", "--count", dest="count", type="int", default=0,
                      help="Max packet count before exiting'",
                      metavar='COUNT')

    parser.add_option("-m", "--mcast-addr", dest="mcast_addr", default="239.193.7.3",
                      help="Comma delimited list of src ip addresses used to filter",
                      metavar="ADDRS")

    parser.add_option("--no-bind", dest="no_bind", action='store_true', default=False,
                      help="Flag to disable port binding, default::False, ie will try to bind")

    parser.add_option("-l", "--log-level", dest="log_level", default='INFO',
                      help="log level: debug, info, warn, critical, ERROR, FATAL, etc. ")

    return parser


def setup_mcast_port_listener(mcast_grp, mcast_port, is_mac=False):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    if is_mac:
        # Mac may need to re-use port to share port, linux may work with re-suse addr above?
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    else:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind((MCAST_GRP, MCAST_PORT))  # use MCAST_GRP instead of '' to listen only
    # to MCAST_GRP, not all groups on MCAST_PORT
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

def listen_on_port(sock, count=None, verbose=False):
    while True:
        print >> sys.stderr, '\nwaiting to receive message'
        data, address = sock.recvfrom(1024)

        print >> sys.stderr, 'received %s bytes from %s' % (len(data), address)
        #    print >>sys.stderr, data


if __name__ == "__main__":
    opt_parser = get_option_parser()
    options, args = opt_parser.parse_args()

    MCAST_GRP = options.mcast_addr
    MCAST_PORT = options.mcast_port
