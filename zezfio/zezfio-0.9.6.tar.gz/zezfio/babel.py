from ctypes import c_int,c_long,c_float,c_double,create_string_buffer
from collections import namedtuple

def strbool2int(b):
  "1 is True, 0 is False"
  if b in 'Tt1':
     return 1
  elif b in 'Ff0':
     return 0
  else:
     raise TypeError("strbool2int : %s should be in (T|F)"%b)

def ljust2(str_,t_interface):
  padding = int(t_interface[5:-1])
  return str_.ljust(padding)

#c_type is for allocate the array for the c binding
Convert = namedtuple("Convert", ["str_size", "c_size", "c_type","py_array_code", "fortran_type", "str2py"])
c2stuff = {
    "bool"   :   Convert(24,  4,  c_int,    'i', "LOGICAL",          strbool2int ),
    "int"    :   Convert(24,  4,  c_int,    'i', "INTEGER",          int         ),
    "long"   :   Convert(24,  8,  c_long,   'l', "INTEGER*8",        int         ),
    "float"  :   Convert(24,  4,  c_float,  'f', "REAL",             float       ),
    "double" :   Convert(32,  8,  c_double, 'd', "DOUBLE PRECISION", float       )
}

for i in range(3000):
  c2stuff["char[%d]"%i] = Convert(i+1,i,create_string_buffer,'c', "CHARACTER*(%d)"%i, ljust2)

def is_raw(t_interface):
  return "raw" in t_interface

def is_char(t_interface):
  return "char[" in t_interface

def is_string(t_interface):
  return any([is_char(t_interface),is_raw(t_interface)])

from operator import mul
def shape2len(l):
  return reduce(mul, l)

def len2bytes(t_interface,len_=-1,str_=None):

  if is_string(t_interface):
    return len(str_)
  else:
    nele = len_ if len_ != -1 else 1
    return c_int(c2stuff[t_interface].c_size*nele)

import array
def bytes2interface(t_interface,bytes):

  if is_string(t_interface):
    return bytes

  try:
    code = c2stuff[t_interface].py_array_code
  except KeyError:
    raise KeyError("Cannot convert %s into array"%t_interface) 
  else:  
    return array.array(code,bytes)
  
#Interface2byte is create by pyzmq

#We need the len because, if the data_interface is a c_pointer it's not iterable!
#We always receive a array. But if we now it is a scalar (len_=-1) just return
#the first element
def interface2py(data_interface,len_=-1):
  if len_ != -1:
    return [data_interface[i] for i in range(len_)]
  else:
    return data_interface[0]

#Convert:
# string    -> string
# py_scalar -> Array
# py_list   -> Array
def py2interface(t_interface,data_py):

  if is_string(t_interface):
    return data_py

  try:
    code = c2stuff[t_interface].py_array_code
  except KeyError:
    raise KeyError("Cannot convert %s into array"%t_interface) 
    
  if type(data_py) is list:  
    data_py_array = data_py
  else:
    data_py_array = [data_py]

  return array.array(code,data_py_array)  

def py2ascii(data_py):
  try:
    l = map(str,data_py)
  except TypeError:
    return str(data_py)
  else:
    return ",".join(l)

def ascii2py(t_interface,data_ascii,len_=-1):

  if is_raw(t_interface):
    return data_ascii

  try:
    code = c2stuff[t_interface].str2py
  except KeyError:
    raise KeyError("Cannot convert %s into py"%t_interface)

  if is_char(t_interface):
    #We do padding
    return code(data_ascii, t_interface)
  else:
    l_data = data_ascii.split(',')
    return map(code,l_data)

def ascii2interface(t_interface,data_ascii):

  data_py = ascii2py(t_interface,data_ascii)
  return py2interface(t_interface,data_py)

def type_fortran2c(t_fortran):
    for ctype, t in c2stuff.iteritems():
        if t_fortran.lower() == t.fortran_type.lower():
            return ctype
    raise AttributeError, "No C type for Fortran type: %s" % t_fortran

