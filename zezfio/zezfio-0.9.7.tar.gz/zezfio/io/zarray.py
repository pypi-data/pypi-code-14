import os
dir_path = os.path.dirname(os.path.realpath(__file__))
dll_path = os.path.join(dir_path,"gz2ar.so")

from ctypes import CDLL, get_errno
#Absolute path
dll = CDLL(dll_path,use_errno=True)


from zezfio import babel
from ctypes import c_char

d_erno = {100: "gzopen failed for {file}",
          101: "Your buffer size is to small for the uncompressed data for file {file}",
          102: "There are more values to read than (>{length} asked)",
          103: "I have read less values than requested (<{length})",
          104: "Only 1 or 0 are convertible to bool"}

def check_errno():
    errno = get_errno()
    try:
        message_template = d_erno[errno]
    except KeyError:
        return True
    else:
        message = message_template.format(**locals())
        raise BytesWarning("Error: %s"%message)

def gzip2buffer(file,bytes,header_bytes=200):

    total_bytes = header_bytes + bytes
    buffer_type = (c_char * total_bytes)
    buffer = buffer_type()

    dll.gzip2buffer(file,total_bytes,buffer)
    
    if check_errno():
        return buffer

#This function is IMPURE !!! Buffer will be modified !
def buffer2stuff_impure(t_interface,buffer,length):

    if not babel.is_char(t_interface):

        #Get the C function
        try:
            c_function = getattr(dll,"buffer2%s_impure"%t_interface)
        except AttributeError:
            raise 
            raise BytesWarning("Error: No C function to convert your buffer in this format: %s"%t_interface)
        #Malloc the c_array
        try:
            c_type = babel.c2stuff[t_interface].c_type
        except:
            raise BytesWarning("Error: No C_type related to: %s"%t_interface)
        else:
            c_array_type = ( c_type * length)
            c_array = c_array_type()
         
        #Call the function
        c_function(buffer,length,c_array)

    else:
        #Get the C function
        c_function = getattr(dll,"buffer2char")
    
        #Malloc the c_array
        from ctypes import c_char
        char_size = babel.c2stuff[t_interface].c_size

        real_length = length*char_size

        c_array_type = ( c_char * real_length)
        c_array = c_array_type()
    
        #Call the function
        from ctypes import c_size_t
        c_function(buffer, length,c_size_t(char_size), c_array)

    if check_errno():
        return c_array


import gzip

def db2interface(path,t_interface,nele):
    with gzip.open(path,"r") as f:
        f.readline()
        shape = map(int,f.readline().split())
        dlen = babel.shape2len(shape)

    if dlen != nele:
        raise BytesWarning("Error: Asked number of elements (%s) differ from the file header (%s)"%(dlen,nele))

    try:
        str_length = nele * babel.c2stuff[t_interface].str_size
    except KeyError:
        raise TypeError("Error: No size for %s" % t_interface)
    else:
        buffer = gzip2buffer(path,str_length)

    return buffer2stuff_impure(t_interface,buffer,nele) 


#Need to be and array or a string
def interface2db(path, shape, t_interface, data_interface):

    header = [str(len(shape)), 
              "  ".join(map(str,shape))]

    if babel.is_char(t_interface):
        lstr = "".join(data_interface).split('\x00')
    else:
        lstr = map(str,data_interface.tolist())        

    with gzip.open(path, 'w') as f:
        f.write("%s\n" % "\n".join(header+lstr))
