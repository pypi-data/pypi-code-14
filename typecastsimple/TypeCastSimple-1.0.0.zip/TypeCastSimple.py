# coding: utf-8

import binascii
import serial
import sys

from ctypes import *

def TypeFactory(Type, Size = 1):
    if Type == "UCHAR":
        tmp = c_ubyte()
        return tmp
    if Type == "UCHAR *":
        tmp = c_char_p(b"/0")
        tmp = create_string_buffer(Size)
    return tmp
