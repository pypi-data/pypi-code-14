#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
validate_cli.py
^^^^^^^^^^^^^^^

Command line interface for wwPDB OneDep validation webservice API.

:copyright: @wwPDB
:license: Apache 2.0, see LICENSE file for more details.



Updates:
    22-Sep-2016 jdw  adapt for onedep package
    24-Sep-2016 jdw  revise error handling
    28-Sep-2016 jdw  add exp_method argument
    30-Sep-2016 jdw  add additional path conditioning -

"""
from __future__ import print_function
from __future__ import unicode_literals

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"


import logging
import datetime
import sys
import six
import os.path


try:
    from argparse import ArgumentParser as ArgParser
    from argparse import RawTextHelpFormatter
except ImportError:
    from optparse import OptionParser as ArgParser

from onedep import __version__
from onedep import __apiUrl__

from onedep.api.Register import Register
from onedep.api.Validate import Validate


log = logging.getLogger()


def print_(s):
    sys.stdout.write(s)


def version():
    """Print the version and exit"""
    raise SystemExit(__version__)


def readApiKey(filePath):
    apiKey = None
    try:
        fn = os.path.expanduser(filePath)
        with open(fn, 'r') as fp:
            apiKey = fp.read()
    except:
        pass
    return apiKey


def writeSessionId(sessionId, filePath):
    try:
        fn = os.path.expanduser(filePath)
        with open(fn, 'w') as fp:
            fp.write(sessionId)
        return True
    except:
        raise SystemExit("Error writing file %r" % filePath)


def readSessionId(filePath):
    sessionId = None
    try:
        fn = os.path.expanduser(filePath)
        log.debug("Getting session from %r" % fn)
        with open(fn, 'r') as fp:
            sessionId = fp.read()
    except:
        log.debug("failing for file path %r" % filePath)

    return sessionId


def displayStatus(sD, exitFlag=False, exitOnError=True):

    if 'onedep_error_flag' in sD and sD['onedep_error_flag']:
        print_("OneDep error: %s\n" % sD['onedep_status_text'])
        if exitOnError:
            raise SystemExit()
    else:
        if 'status' in sD:
            print_("OneDep status: %s\n" % sD['status'])
    if exitFlag:
        raise SystemExit()


def displayIndex(sD):
    #
    print_("\nOneDep Session File Index:\n")
    try:
        val = Validate()
        ctL = val.getContentTypes()
        if 'index' in sD and len(sD) > 0:
            print_("%25s : %-25s\n" % ("Content Type", "Session File Name"))
            print_("%25s : %-25s\n" % ("------------", "-----------------"))
            for ky in sD['index']:
                if ky in ctL:
                    fn, fmt = sD['index'][ky]
                    print_("%25s : %-25s\n" % (ky, fn))
        else:
            print_("No session content\n")
    except:
        print_("Error processing session index")


def displayActivity(sD):
    #
    format = "%a %b %d %H:%M:%S %Y"
    print_("\nOneDep Request Activity Summary:\n")
    try:
        val = Validate()
        if 'activity_summary' in sD and len(sD) > 0:
            print_("%25s : %-25s\n" % ("Category    ", "Count            "))
            print_("%25s : %-25s\n" % ("------------", "-----------------"))
            for ky in sD['activity_summary']:
                if ky not in ['session_list']:
                    val = sD['activity_summary'][ky]
                    print_("%25s : %-25s\n" % (ky, val))
            if 'session_list' in sD['activity_summary']:
                print_("\n%-25s : %-10s: %-25s: %-45s\n" % (" Session Creation Time", "Status    ", "Time after submit (secs)", "Session Identifier"))
                print_("%25s : %-10s: %-25s: %-45s\n" % ("------------------------", "----------", "------------------------ ", "----------------------------------------"))
                for s in sD['activity_summary']['session_list']:
                    tiso = s[1]
                    dt = datetime.datetime.strptime(tiso[:19], '%Y-%m-%dT%H:%M:%S')
                    fdt = dt.strftime(format)
                    if s[3] == "0" or s[3] == 0:
                        print_("%25s : %-10s: %24s : %-45s\n" % (fdt, s[2], "", s[0]))
                    else:
                        print_("%25s : %-10s: %24.2f : %-45s\n" % (fdt, s[2], s[3], s[0]))

        else:
            print_("No session activity data\n")
    except:
        print_("Error processing activity summary")


def filterPath(inpPath):
    try:
        return os.path.expanduser(inpPath)
    except:
        return inpPath


def run():
    """ Command line interface for OneDep validation API """

    description = """
    Command line interface for OneDep validation API:

    Step 1:  Request a OneDep API access Key.  API keys are sent to your e-mail\n
            address and are valid for 2 days.

        onedep_validate --register --email <user@hostname>

            For convenience, the API access key may be stored in a hidden file
            in your home directory. Copy the API access key e-mail attachment
            as follows.

        cp onedep_apikey.jwt ~/.onedep_apikey.jwt

    Step 2:  Request a new session on the validation server.

        onedep_validate --new_session

            By default, session information will be stored in your home directory
            in file ~/.onedep_current_session

    Step 3:  Upload the target data files for validation

        X-ray:

            onedep_validate --input_file 1abc.cif        --input_type model
            onedep_validate --input_file 1abc-sf.cif.gz  --input_type structure-factors

        NMR:
            onedep_validate --input_file 1abc.cif            --input_type model
            onedep_validate --input_file 1abc-shifts.cif.gz  --input_type nmr-chemical-shifts

        3DEM:
            onedep_validate --input_file 1abc.cif            --input_type model
            onedep_validate --input_file 1abc-vol.map.gz     --input_type em-volume

    Step 4:  Submit a reqest to validate the data files in the current session

            onedep_validate --validate

    Step 5:  Check the status of the validation service request

            onedep_validate --status

    Step 6: When the request is completed, recover the validation report and data files.


            onedep_validate --output_file report.pdf  --output_type validation-report-full
            onedep_validate --output_file report.xml  --output_type validation-data

    """
    try:
        parser = ArgParser(description=description, formatter_class=RawTextHelpFormatter)
    except:
        parser = ArgParser(description="Command line interface for OneDep validation API")

    # For optparse.OptionParser add an `add_argument` method for compatibility with argparse.ArgumentParser
    try:
        parser.add_argument = parser.add_option
    except AttributeError:
        pass
    #

    parser.add_argument('--email',
                        type=six.text_type,
                        default=None,
                        help="e-mail address to receive OneDep API key")

    parser.add_argument('--register', action='store_true', dest='register', default=False,
                        help='Register to receive a OneDep API by e-mail')
    ##
    parser.add_argument('--session_file',
                        dest="sessionFile",
                        type=six.text_type,
                        default=filterPath("~/.onedep_current_session"),
                        help="File containing current session information (default: %(default)s)")
    ##
    parser.add_argument('--api_key_file',
                        dest="apiKeyFile",
                        type=six.text_type,
                        default=filterPath("~/.onedep_apikey.jwt"),
                        help="File containing a OneDep API key (default: %(default)s)")
    #
    parser.add_argument('--new_session',
                        dest="newSessionOp",
                        action='store_true',
                        default=False,
                        help="Start a new session")
    ##
    parser.add_argument('--input_file',
                        dest="inputFile",
                        type=six.text_type,
                        default=None,
                        help="Input file path")

    parser.add_argument('--input_type',
                        dest='inputType',
                        type=six.text_type,
                        default='model',
                        choices=['model', 'structure-factors', 'nmr-chemical-shifts', 'nmr-restraints', 'em-volume'],
                        help="Input file type")
    ##
    parser.add_argument('--exp_method',
                        dest='expMethod',
                        type=six.text_type,
                        default=None,
                        choices=['X-RAY', 'NMR', 'EM'],
                        help="Use a validation protocol for this experimental method")
    parser.add_argument('--validate',
                        dest="validateOp",
                        action='store_true',
                        default=False,
                        help="Submit a request to run the validation service")
    ##
    parser.add_argument('--status',
                        dest="statusOp",
                        action='store_true',
                        default=False,
                        help="Get the status of the current session")
    #
    parser.add_argument('--test_complete',
                        dest="completeOp",
                        action='store_true',
                        default=False,
                        help="Return competion status for the current session [1 for done or 0 otherwise]")
    #
    parser.add_argument('--output_file',
                        dest="outputFile",
                        type=six.text_type,
                        default=None,
                        help="Output file path")

    parser.add_argument('--output_type',
                        dest='outputType',
                        type=six.text_type,
                        default='validation-report-full',
                        choices=['validation-report-full', 'validation-data', 'validation-report-log'],
                        help="Output file type")
    ##
    parser.add_argument('--index',
                        dest='indexOp',
                        action='store_true',
                        default=False,
                        help="Request index of the data files in the current session")
    #
    parser.add_argument('--activity',
                        dest='activityOp',
                        action='store_true',
                        default=False,
                        help="Request a summary of service requests")
    #
    parser.add_argument('--version', action='store_true', help='Show the version number and exit')

    ##
    parser.add_argument('--verbose', action='store_true', help='Set verbose logging')
    parser.add_argument('--debug', action='store_true', help='Set debug logging')
    parser.add_argument('--test_mode', dest='testMode', action='store_true', help='Set service in test mode')
    parser.add_argument('--test_duration',
                        dest="testModeDuration",
                        type=int,
                        default=10,
                        help="Mock service duration in test mode (seconds, default=10)")
    parser.add_argument('--log_file',
                        dest="logFile",
                        type=six.text_type,
                        default=None,
                        help="Log file path")

    parser.add_argument('--api_url',
                        dest="apiUrl",
                        type=six.text_type,
                        default=__apiUrl__,
                        help="API base URL")
    #
    options = parser.parse_args()
    if isinstance(options, tuple):
        args = options[0]
    else:
        args = options
    del options

    # Print the version and exit
    if args.version:
        version()
    #
    # Configure logging -
    logging.captureWarnings(True)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s')
    logging.basicConfig(format='%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s')
    if args.logFile:
        handler = logging.FileHandler(args.logFile)
        handler.setFormatter(formatter)
        log.addHandler(handler)
    #
    if args.debug:
        log.setLevel(logging.DEBUG)
        log.debug("debug logging activated")
    elif args.verbose:
        log.setLevel(logging.INFO)
        log.debug("info logging activated")
    else:
        log.setLevel(logging.ERROR)

    #
    apiUrl = args.apiUrl
    #
    # Register for a new API key and exit -
    if args.register and args.email:
        reg = Register(apiUrl=apiUrl)
        rD = reg.register(email=args.email)
        displayStatus(rD, exitFlag=True)
    #
    # Read API key file -
    apiKey = None
    if args.apiKeyFile:
        apiKey = readApiKey(args.apiKeyFile)
        if not apiKey:
            parser.print_usage()
            raise SystemExit("\nError reading Api key file %s" % filterPath(args.apiKeyFile))

    # Create a new session or recover cached session data -
    sessionId = None
    if args.newSessionOp:
        val = Validate(apiKey=apiKey, apiUrl=apiUrl)
        rD = val.createSession()
        displayStatus(rD)
        sessionId = rD['session_id']
        writeSessionId(sessionId, args.sessionFile)
    else:
        sessionId = readSessionId(args.sessionFile)
        if not sessionId:
            parser.print_usage()
            raise SystemExit("\nError reading session file %s" % filterPath(args.sessionFile))

    # Input files -
    if args.inputFile and args.inputType:
        val = Validate(apiKey=apiKey, apiUrl=apiUrl)
        val.setSession(sessionId)
        fmt = val.getContentFormatDefault(args.inputType)
        rD = val.inputFile(filePath=filterPath(args.inputFile), contentType=args.inputType, fileFormat=fmt)
        displayStatus(rD)

    # Output files -
    if args.outputFile and args.outputType:
        val = Validate(apiKey=apiKey, apiUrl=apiUrl)
        val.setSession(sessionId)
        rD = val.getOutputByType(filePath=filterPath(args.outputFile), contentType=args.outputType)
        displayStatus(rD)

    # Submit validation service request -
    if args.validateOp:
        pD = {}
        val = Validate(apiKey=apiKey, apiUrl=apiUrl)
        val.setSession(sessionId)
        # optional test mode configuration
        if args.testMode:
            pD['worker_test_mode'] = True
        if args.testModeDuration:
            pD['worker_test_duration'] = args.testModeDuration
        else:
            pD['worker_test_duration'] = 10
        #
        if args.expMethod:
            pD['exp_method'] = args.expMethod
        #
        rD = val.run(**pD)
        displayStatus(rD)

    # Get index of session file content -
    if args.indexOp:
        val = Validate(apiKey=apiKey, apiUrl=apiUrl)
        val.setSession(sessionId)
        rD = val.getIndex()
        displayStatus(rD)
        displayIndex(rD)

    if args.activityOp:
        val = Validate(apiKey=apiKey, apiUrl=apiUrl)
        val.setSession(sessionId)
        rD = val.getActivity()
        displayStatus(rD)
        displayActivity(rD)

    # Get session service status details -
    if args.statusOp:
        val = Validate(apiKey=apiKey, apiUrl=apiUrl)
        val.setSession(sessionId)
        rD = val.getStatus()
        displayStatus(rD)

    if args.completeOp:
        val = Validate(apiKey=apiKey, apiUrl=apiUrl)
        val.setSession(sessionId)
        rD = val.getStatus()
        if 'status' in rD and rD['status'] in ['completed', 'failed']:
            iRet = 1
            print_("%d" % iRet)
        else:
            iRet = 0
            print_("%d" % iRet)
    #


if __name__ == '__main__':
    run()
