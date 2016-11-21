# coding: utf-8

import binascii
import sys, os

from ctypes import *

def DcWinDll(dllPath):
    try:
        dll=WinDLL(dllPath)
    except Exception as e:
        try:
            dll = WinDLL(os.path.join(os.path.dirname(dllPath), os.path.pardir, os.path.basename(dllPath)))
        except Exception as e:
            print(e)
            sys.exit(1)
    return dll
