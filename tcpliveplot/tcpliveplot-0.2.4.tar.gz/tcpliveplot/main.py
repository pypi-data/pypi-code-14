#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import signal

from .utils.utilty import Utility
from .tcpliveplot import TcpLivePlot
from .info_registry import InfoRegistry


# constants
TCP_PLOT_VERSION = "0.2.4"
TCP_LOG_FORMAT_VERSION_MIN = "2"

DEFAULT_LOGFILE_PATH = "/tmp/tcplog.log"
DEFAULT_INPUT_BACKEND = "socket"

# default values
DEFAULT_SOCKETSERVER_PORT = 11337
DEFAULT_SOCKETSERVER_LOCATION = 'localhost:' + str(DEFAULT_SOCKETSERVER_PORT)
DEFAULT_LINES_TO_SHOW = ['cwnd']
DEFAULT_FILTER_PORT = 5001

# move
VALUES_TO_PLOT = ['cwnd', 'sst', 'rtt', 'bw'] # (only values for Y-axis)

# main prog
def main():
    inputBackend = None
    guiBackend = None
    infoRegistry = InfoRegistry()
    options = parse_options()
    startupSelfCheck(options)

    if(options.showVersion):
        print("TCPlivePLOT: " + TCP_PLOT_VERSION)
        sys.exit(0)

    options.guiBackend = "live"

    # init input backend
    if(options.inputBackend == "socket"):
        from .backends.input.socket import SocketInput
        inputBackend = SocketInput(options, infoRegistry)
    elif(options.inputBackend == "file"):
        from .backends.input.file import FileInput
        inputBackend = FileInput(options, infoRegistry)
    # elif(options.inputBackend == "stdin"):
    #     from .backends.input.stdin import StdinInput
    #     inputBackend = StdinInput(options, info)

    if(inputBackend is None):
        print("No valid input backend selected. Exiting...")
        sys.exit(1)

    # init guiBackend
    if(options.guiBackend == "live"):
        from .backends.gui.live import LiveGui
        guiBackend = LiveGui(options, infoRegistry)
    else:
        pass

    if(guiBackend is None):
        print("No valid GUI backend selected. Exiting...")
        sys.exit(1)

    if(inputBackend is not None):
        inputBackend.startupCheck()
        inputBackend.startUp()

    if(guiBackend is not None):
        guiBackend.startupCheck()
        guiBackend.startUp()

    tcpLivePlot = TcpLivePlot(inputBackend, guiBackend, options, infoRegistry)
    signal.signal(signal.SIGINT, tcpLivePlot.handleSignals)
    signal.signal(signal.SIGTERM, tcpLivePlot.handleSignals)
    tcpLivePlot.run()
    # try:
    #     tcpLivePlot = TcpLivePlot(inputBackend, guiBackend, options, infoRegistry)
    #     signal.signal(signal.SIGINT, tcpLivePlot.handleSignals)
    #     signal.signal(signal.SIGTERM, tcpLivePlot.handleSignals)
    #     tcpLivePlot.run()
    #     # ^-- starts the main programme
    # except Exception as e:
    #     Utility.eprint(str(e))
    #     raise e
    # finally:
    #     if(not options.quiet):
    #         print("Goodbye cruel world!")
    #     sys.exit(0)


def parse_options():
    parser = argparse.ArgumentParser()

    parser.add_argument(
            "-i",
            "--input-backend",
            help="Available input backends: \"socket\" and \"file\" (default: " + DEFAULT_INPUT_BACKEND + ")",
            dest="inputBackend",
            default=DEFAULT_INPUT_BACKEND)

    # TODO: remove
    parser.add_argument(
            "-b",
            "--buffer", help="Length of preload buffer (in seconds, default: 1, 0 to deactivate preload buffer)",
            type=float,
            dest="preloadBuffer",
            default=1)

    # TODO: remove
    parser.add_argument(
            "-ib",
            "--interimbuffer", help="Activate interim buffering.",
            action="store_true",
            dest="interimBuffering",
            default=False)

    # TODO: remove
    parser.add_argument(
            "-ps",
            "--playback-speed", help="Playback speed (factor, default: 1)",
            type=float,
            dest="playbackSpeed",
            default=1)

    # TODO: remove
    parser.add_argument(
            "-aps",
            "--adaptive-playback-speed", help="Enable adaptive playback speed (default: false)",
            action="store_true",
            dest="adaptivePlaybackSpeed",
            default=False)

    # TODO: remove
    parser.add_argument(
            "--buffer-size", help="Number of elements to buffer from socket per filter (5000)",
            dest="bufferLength",
            default=5000)

    parser.add_argument(
            "-4",
            "--useQt4", help="Use Qt-4 instead of Qt-5 (default) as matplotlib-backend  (default: False)",
            action="store_true",
            dest="useQt4",
            default=False)

    parser.add_argument(
            "-z",
            "--blit", help="Activate blitting for better performance - but broken axis labels (default: False)",
            action="store_true",
            dest="blitting",
            default=False)

    logTypeGroup = parser.add_mutually_exclusive_group()

    logTypeGroup.add_argument(
            "-s",
            "--server",
            help="IP and Port of socket-logging server (" + DEFAULT_SOCKETSERVER_LOCATION + ")",
            dest="logServer",
            default=DEFAULT_SOCKETSERVER_LOCATION)
    logTypeGroup.add_argument(
            "-f",
            "--filepath",
            help="Path where the log file is stored - only usable with file input-backend (default: " + DEFAULT_LOGFILE_PATH + ")",
            type=str,
            default=DEFAULT_LOGFILE_PATH,
            dest="logFilePath")

    # TODO: remove as param
    parser.add_argument(
            "-df",
            help="Number of FPS to draw",
            dest="drawFps",
            type=int,
            default=60)
    parser.add_argument(
            "-di",
            help="Draw intervall",
            dest="drawIntervall",
            type=int,
            default=100)

    parser.add_argument(
            "-x",
            help="Seconds to plot (default: 20)",
            dest="xDelta",
            type=int,
            default=20)

    parser.add_argument(
            "-y",
            help="Static Y-axis (default: 0 = auto)",
            dest="yAxisMax",
            type=int,
            default=0)


    # TODO: remove as param
    parser.add_argument(
            "-r",
            "--resolution",
            help="Plot resolution (in seconds, default: 0.01)",
            dest="plotResolution",
            type=float,
            default=0.1)

    # Filter
    parser.add_argument(
            "-p",
            "--port",
            help="Filter by port. Multiple occurrences possible (" + str(DEFAULT_FILTER_PORT) + ")",
            dest="filterPorts",
            action='append',
            type=int,
            default=[])


    parser.add_argument(
            "-d",
            "--debug", help="Debug mode - ignores quiet mode (default: false)",
            action="store_true",
            dest="debug",
            default=False)

    parser.add_argument(
            "-q",
            "--quiet", help="Whether to ouput anything at all on console (default: false)",
            action="store_true",
            dest="quiet",
            default=False)

    parser.add_argument(
            "--version",
            help="Print version information",
            action="store_true",
            dest="showVersion",
            default=False)

    options = parser.parse_args()

    return options

def startupSelfCheck(options):
    pass

if __name__ == "__main__":
    main()
