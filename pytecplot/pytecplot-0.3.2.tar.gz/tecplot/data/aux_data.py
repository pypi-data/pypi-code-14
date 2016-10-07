from ..tecutil import _tecutil, log_setattr
from .. import layout
from ..tecutil import util

@log_setattr
class AuxData(object):
    def __init__(self, frame):
        self.frame = frame
        with frame.activated():
            self.handle = _tecutil.AuxDataFrameGetRef()

    def item(self, i):
        """item by number"""
        return util.AuxDataGetItemByNumber(self.handle, i+1)

    def __getitem__(self, key):
        return util.AuxDataGetItemByName(self.handle, key)

    def __len__(self):
        return _tecutil.AuxDataGetNumItems(self.handle)

@property
def aux_data(frame):
    """Returns the auxiliary data object.

    :type: `data.AuxData`

    This is a generic container for arbitrary data attached to this
    `Frame`. See `AuxData` for more details.
    """
    return AuxData(frame)

layout.Frame.aux_data = aux_data

def AuxDataGetItemByNumber(self, auxdata, number):
    _ctype = {AuxDataType.String: c_char_p}
    name = c_char_p()
    val = c_void_p()
    valtype = c_int()
    retain = c_bool()
    _tecutil.handle.tecUtilAuxDataGetItemByIndex(auxdata, number, byref(name), byref(val),
                                             byref(valtype), byref(retain))
    name = name.value.decode()
    result = ctypes.cast(val, _ctype[AuxDataType(valtype.value)])
    if isinstance(result, c_char_p):
        result = result.value.decode()
    else:
        result = result.value
    return name, result



def AuxDataGetItemByName(self, auxdata, name):
    _ctype = {AuxDataType.String : c_char_p}
    val = c_void_p()
    valtype = c_int()
    retain = c_bool()
    success = _tecutil.handle.tecUtilAuxDataGetItemByName(auxdata, name.encode(), byref(val),
                                                      byref(valtype), byref(retain))
    if not success:
        raise KeyError
    result = ctypes.cast(val, _ctype[AuxDataType(valtype.value)])
    if isinstance(result, c_char_p):
        result = result.value.decode()
    return result
