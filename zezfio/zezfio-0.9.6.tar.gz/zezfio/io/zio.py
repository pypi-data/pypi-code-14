import zscalar
import zarray
from zezfio import babel
import os

def db2interface(path,t_interface,len_):

    if babel.is_raw(t_interface):
        with open(path, 'r') as f:
            data = f.read()
        return data
    elif len_ == -1:
        return zscalar.db2interface(path,t_interface)
    else:
        return zarray.db2interface(path, t_interface, len_)


#Data_interface is a string or and array
def interface2db(path,t_interface,shape,data_interface):

    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    if babel.is_raw(t_interface):
        with open(path, 'w') as f:
            f.write("%s\n" % data_interface)
    elif shape == [-1]:
        zscalar.interface2db(path,data_interface)
    else:
        zarray.interface2db(path,shape, t_interface, data_interface)



