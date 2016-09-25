# -*- coding: utf-8 -*-
'''
This module provides system information through query of wmic Windows command.

Author:      Bartek Rybak
Copyright:   Copyright (c) 2016 Bartek Rybak    
License:     MIT
Version:     1.0.0
Build:       2016.09.25 14:45:16
''' 
__version__ = '1.0.0'

import platform
if platform.system().lower() != "windows":
    raise ImportError('Module ' + __name__ + ' can be used on Windows platform only.')
import sys
import subprocess
from enum import Enum
import re
import inspect

__all__ = ['query', 'Category', 'QueryError', 'getmeta']

_myname = lambda: inspect.stack()[1][3]

def getmeta(metavariable = None):
    ''' Return module metadata.
        Keyword arguments:
            metavariable - requested metadata variable as string {"author", "copyright", "license", "version", "build"} 
                           or None (default None).
                           
        Function returns metadata as string according to metavariable or 
        dictionary of all available module metadata if metavariable is None. 
    '''
    metadomain = ["author", "copyright", "license", "version", "build"]
    if metavariable is None:
        meta = {}
        for d in metadomain:
            v = getmeta(d)
            if v is not None:
                meta[d] = v
        return meta
    if metavariable not in metadomain:
        raise ValueError("Wrong metavariable '{}'".format(metavariable))
        
    m = re.search(r'^' +metavariable + ':\s*(.*?)\s*$', __doc__, flags = re.MULTILINE | re.IGNORECASE)
    if m is not None and m.lastindex > 0:
        return m.group(1)
    return None


class QueryError(Exception):
    '''   Exception raised on query errors when exception_on_error = True. '''
    pass

class Category(str,  Enum):
    '''   An enumeration defining domain of possible information requests through query function. '''
    BASEBOARD = "BASEBOARD",  # Base board (also known as a motherboard or system board) management.
    BIOS = "BIOS",  # Basic input/output services (BIOS) management.
    BOOTCONFIG = "BOOTCONFIG",  # Boot configuration management.
    CDROM = "CDROM",  # CD-ROM management.
    COMPUTERSYSTEM = "COMPUTERSYSTEM",  # Computer system management.
    CPU = "CPU",  # CPU management.
    CSPRODUCT = "CSPRODUCT",  # Computer system product information from SMBIOS. 
    DATAFILE = "DATAFILE",  # DataFile Management.  
    DCOMAPP = "DCOMAPP",  # DCOM Application management.
    DESKTOP = "DESKTOP",  # User's Desktop management.
    DESKTOPMONITOR = "DESKTOPMONITOR",  # Desktop Monitor management.
    DEVICEMEMORYADDRESS = "DEVICEMEMORYADDRESS",  # Device memory addresses management.
    DISKDRIVE = "DISKDRIVE",  # Physical disk drive management. 
    DISKQUOTA = "DISKQUOTA",  # Disk space usage for NTFS volumes.
    DMACHANNEL = "DMACHANNEL",  # Direct memory access (DMA) channel management.
    ENVIRONMENT = "ENVIRONMENT",  # System environment settings management.
    FSDIR = "FSDIR",  # Filesystem directory entry management. 
    GROUP = "GROUP",  # Group account management. 
    IDECONTROLLER = "IDECONTROLLER",  # IDE Controller management.  
    IRQ = "IRQ",  # Interrupt request line (IRQ) management. 
    JOB = "JOB",  # Provides  access to the jobs scheduled using the schedule service. 
    LOADORDER = "LOADORDER",  # Management of system services that define execution dependencies. 
    LOGICALDISK = "LOGICALDISK",  # Local storage device management.
    LOGON = "LOGON",  # LOGON Sessions.  
    MEMCACHE = "MEMCACHE",  # Cache memory management.
    MEMORYCHIP = "MEMORYCHIP",  # Memory chip information.
    MEMPHYSICAL = "MEMPHYSICAL",  # Computer system's physical memory management. 
    NETCLIENT = "NETCLIENT",  # Network Client management.
    NETLOGIN = "NETLOGIN",  # Network login information (of a particular user) management. 
    NETPROTOCOL = "NETPROTOCOL",  # Protocols (and their network characteristics) management.
    NETUSE = "NETUSE",  # Active network connection management.
    NIC = "NIC",  # Network Interface Controller (NIC) management.
    NICCONFIG = "NICCONFIG",  # Network adapter management. 
    NTDOMAIN = "NTDOMAIN",  # NT Domain management.  
    NTEVENT = "NTEVENT",  # Entries in the NT Event Log.  
    NTEVENTLOG = "NTEVENTLOG",  # NT eventlog file management. 
    ONBOARDDEVICE = "ONBOARDDEVICE",  # Management of common adapter devices built into the motherboard (system board).
    OS = "OS",  # Installed Operating System/s management. 
    PAGEFILE = "PAGEFILE",  # Virtual memory file swapping management. 
    PAGEFILESET = "PAGEFILESET",  # Page file settings management. 
    PARTITION = "PARTITION",  # Management of partitioned areas of a physical disk.
    PORT = "PORT",  # I/O port management.
    PORTCONNECTOR = "PORTCONNECTOR",  # Physical connection ports management.
    PRINTER = "PRINTER",  # Printer device management. 
    PRINTERCONFIG = "PRINTERCONFIG",  # Printer device configuration management.  
    PRINTJOB = "PRINTJOB",  # Print job management. 
    PROCESS = "PROCESS",  # Process management. 
    PRODUCT = "PRODUCT",  # Installation package task management. 
    QFE = "QFE",  # Quick Fix Engineering.  
    QUOTASETTING = "QUOTASETTING",  # Setting information for disk quotas on a volume. 
    RDACCOUNT = "RDACCOUNT",  # Remote Desktop connection permission management.
    RDNIC = "RDNIC",  # Remote Desktop connection management on a specific network adapter.
    RDPERMISSIONS = "RDPERMISSIONS",  # Permissions to a specific Remote Desktop connection.
    RDTOGGLE = "RDTOGGLE",  # Turning Remote Desktop listener on or off remotely.
    RECOVEROS = "RECOVEROS",  # Information that will be gathered from memory when the operating system fails. 
    REGISTRY = "REGISTRY",  # Computer system registry management.
    SCSICONTROLLER = "SCSICONTROLLER",  # SCSI Controller management.  
    SERVER = "SERVER",  # Server information management. 
    SERVICE = "SERVICE",  # Service application management. 
    SHADOWCOPY = "SHADOWCOPY",  # Shadow copy management.
    SHADOWSTORAGE = "SHADOWSTORAGE",  # Shadow copy storage area management.
    SHARE = "SHARE",  # Shared resource management. 
    SOFTWAREELEMENT = "SOFTWAREELEMENT",  # Management of the  elements of a software product installed on a system.
    SOFTWAREFEATURE = "SOFTWAREFEATURE",  # Management of software product subsets of SoftwareElement. 
    SOUNDDEV = "SOUNDDEV",  # Sound Device management.
    STARTUP = "STARTUP",  # Management of commands that run automatically when users log onto the computer system.
    SYSACCOUNT = "SYSACCOUNT",  # System account management.  
    SYSDRIVER = "SYSDRIVER",  # Management of the system driver for a base service.
    SYSTEMENCLOSURE = "SYSTEMENCLOSURE",  # Physical system enclosure management.
    SYSTEMSLOT = "SYSTEMSLOT",  # Management of physical connection points including ports,  slots and peripherals, and proprietary connections points.
    TAPEDRIVE = "TAPEDRIVE",  # Tape drive management.  
    TEMPERATURE = "TEMPERATURE",  # Data management of a temperature sensor (electronic thermometer).
    TIMEZONE = "TIMEZONE",  # Time zone data management. 
    UPS = "UPS",  # Uninterruptible power supply (UPS) management. 
    USERACCOUNT = "USERACCOUNT",  # User account management.
    VOLTAGE = "VOLTAGE",  # Voltage sensor (electronic voltmeter) data management.
    VOLUME = "VOLUME",  # Local storage volume management.
    VOLUMEQUOTASETTING = "VOLUMEQUOTASETTING",  # Associates the disk quota setting with a specific disk volume. 
    VOLUMEUSERQUOTA = "VOLUMEUSERQUOTA",  # Per user storage volume quota management.
    WMISET = "WMISET"  # WMI service operational parameters management. 
    
def query(category = Category.CPU, where = None, attributes = None, exception_on_error = True, debug = False):
    '''    Query system information via Windows system command wmic and return tuple of two items:
        - list of returned attributes (or None),
        - list of dictionaries containing result(s).
    
    Keyword arguments:
        category           -- requested category (domain in enum Category) of information (default Category.CPU)
                              domain defined by enum Category,
        where              -- where clause as defined by WQL (default None),
        attributes         -- list of attributes to be returned in the query result (default None - means all attributes),
        exception_on_error -- throw exception (QueryError) on error (default False),
        debug              -- print debug information on stderr (default False).
    '''
    
    cmd = ["wmic"]
    if isinstance(category, Category):
        cmd.append(category.value)
        print
    else:
        cmd.append(category)
    if where is not None:
        cmd.append("where")
        cmd.append(where)
    cmd.append("get")
    if attributes is not None:
        if isinstance(attributes, list) or isinstance(attributes, tuple) or isinstance(attributes, set):
            cmd.append(",".join(map(str, attributes)))
        else:
            cmd.append(attributes)
    cmd.append("/format:csv")

    if debug:
        print("DEBUG: {}".format(sys.modules[__name__]), file = sys.stderr)
        print("DEBUG: {}.{}: Command: {}".format(__name__, _myname(), cmd), file = sys.stderr)
    
    resultHeader = None
    resultData = []
    try:
        for line in [x.rstrip() for x in subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode(sys.stdout.encoding, 'ignore').split("\n")]:           
            if len(line)> 0:
                wmicResult = line.split(",")
                if resultHeader is None:
                    resultHeader = wmicResult
                else:
                    result = {}
                    for i in range(len(resultHeader)):
                        result[resultHeader[i]] = wmicResult[i]
                    resultData.append(result)
                
    except subprocess.CalledProcessError as e:
        if exception_on_error:
            raise QueryError("System command wmic reported error.", e)
            
    except FileNotFoundError as e:
        if exception_on_error:
            raise QueryError("Cannot find wmic system command.", e)
            
    return (resultHeader, resultData)

def _printHeader(title, filler = "-"):
    l = len(title)
    print(filler * l)
#    print("=  {}  =".format(title))
    print(title)
    print(filler * l)
    return

if __name__ == "__main__":
    _printHeader("Module {}".format(__file__), filler = '=')
    print(__doc__.strip())
    
    for n in __all__:
        o = globals()[n]
        print()
        _printHeader(n)
        print(o.__doc__)
#        help(o)
