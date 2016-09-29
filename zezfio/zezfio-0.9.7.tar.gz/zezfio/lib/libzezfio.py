#!/usr/bin/env python
import zmq
import array

import sys
this = sys.modules[__name__]  
this.socket = None

def zezfio_initialise(address):
    context = zmq.Context()
    this.socket = context.socket(zmq.REQ)
    this.socket.connect(address)

def bytes2int(bytes):
    return array.array("i",bytes).pop()

def zezfio_has(msg):
    s = this.socket

    s.send("has.%s"%msg)
    return bytes2int(s.recv())


def zezfio_get(msg):
    s = this.socket

    s.send("get.%s"%msg)
    
    zerrno = bytes2int(s.recv())
   
    if (zerrno >= 0):
        _ = s.recv()
        return s.recv()

def zezfio_set(msg, bytes):
    s = this.socket

    s.send("set.%s"%msg,zmq.SNDMORE)
    s.send(bytes)
    
    return bytes2int(s.recv())


def zezfio_get_ascii(msg):
    s = this.socket

    s.send("get_ascii.%s"%msg)
    
    zerrno = bytes2int(s.recv())
   
    if (zerrno >= 0):
        return s.recv()

def zezfio_set_ascii(msg,string):
    s = this.socket

    s.send("set_ascii.%s"%msg,zmq.SNDMORE)
    s.send(string)    
    return bytes2int(s.recv())
