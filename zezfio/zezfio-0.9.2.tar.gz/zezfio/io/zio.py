import zscalar
import zarray

def db2interface(path,t_interface,len_):

    if len_ == -1:
        return zscalar.db2interface(path,t_interface)
    else:
        return zarray.db2interface(path, t_interface, len_)


#Data_interface is a string or and array
def interface2db(path,t_interface,shape,data_interface):

    if shape == [-1]:
        zscalar.interface2db(path,data_interface)

    else:
        zarray.interface2db(path,shape, t_interface, data_interface)


