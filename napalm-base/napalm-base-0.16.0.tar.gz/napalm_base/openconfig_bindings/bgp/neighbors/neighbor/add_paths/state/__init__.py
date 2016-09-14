
from operator import attrgetter
import pyangbind.lib.xpathhelper as xpathhelper
from pyangbind.lib.yangtypes import RestrictedPrecisionDecimalType, RestrictedClassType, TypedListType
from pyangbind.lib.yangtypes import YANGBool, YANGListType, YANGDynClass, ReferenceType
from pyangbind.lib.base import PybindBase
from decimal import Decimal
from bitarray import bitarray
class state(PybindBase):
  """
  This class was auto-generated by the PythonClass plugin for PYANG
  from YANG module openconfig-bgp - based on the path /bgp/neighbors/neighbor/add-paths/state. Each member element of
  the container is represented as a class variable - with a specific
  YANG type.

  YANG Description: State information associated with ADD_PATHS
  """
  __slots__ = ('_pybind_generated_by', '_path_helper', '_yang_name', '_extmethods', '__receive','__send_max',)

  _yang_name = 'state'

  _pybind_generated_by = 'container'

  def __init__(self, *args, **kwargs):

    helper = kwargs.pop("path_helper", None)
    if helper is False:
      self._path_helper = False
    elif helper is not None and isinstance(helper, xpathhelper.YANGPathHelper):
      self._path_helper = helper
    elif hasattr(self, "_parent"):
      helper = getattr(self._parent, "_path_helper", False)
      self._path_helper = helper
    else:
      self._path_helper = False

    self._extmethods = False
    self.__receive = YANGDynClass(base=YANGBool, default=YANGBool("false"), is_leaf=True, yang_name="receive", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='boolean', is_config=False)
    self.__send_max = YANGDynClass(base=RestrictedClassType(base_type=int, restriction_dict={'range': ['0..255']}, int_size=8), is_leaf=True, yang_name="send-max", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint8', is_config=False)

    load = kwargs.pop("load", None)
    if args:
      if len(args) > 1:
        raise TypeError("cannot create a YANG container with >1 argument")
      all_attr = True
      for e in self._pyangbind_elements:
        if not hasattr(args[0], e):
          all_attr = False
          break
      if not all_attr:
        raise ValueError("Supplied object did not have the correct attributes")
      for e in self._pyangbind_elements:
        nobj = getattr(args[0], e)
        if nobj._changed() is False:
          continue
        setmethod = getattr(self, "_set_%s" % e)
        if load is None:
          setmethod(getattr(args[0], e))
        else:
          setmethod(getattr(args[0], e), load=load)

  def _path(self):
    if hasattr(self, "_parent"):
      return self._parent._path()+[self._yang_name]
    else:
      return [u'bgp', u'neighbors', u'neighbor', u'add-paths', u'state']

  def _get_receive(self):
    """
    Getter method for receive, mapped from YANG variable /bgp/neighbors/neighbor/add_paths/state/receive (boolean)

    YANG Description: Enable ability to receive multiple path advertisements
for an NLRI from the neighbor or group
    """
    return self.__receive
      
  def _set_receive(self, v, load=False):
    """
    Setter method for receive, mapped from YANG variable /bgp/neighbors/neighbor/add_paths/state/receive (boolean)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_receive is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_receive() directly.

    YANG Description: Enable ability to receive multiple path advertisements
for an NLRI from the neighbor or group
    """
    try:
      t = YANGDynClass(v,base=YANGBool, default=YANGBool("false"), is_leaf=True, yang_name="receive", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='boolean', is_config=False)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """receive must be of a type compatible with boolean""",
          'defined-type': "boolean",
          'generated-type': """YANGDynClass(base=YANGBool, default=YANGBool("false"), is_leaf=True, yang_name="receive", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='boolean', is_config=False)""",
        })

    self.__receive = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_receive(self):
    self.__receive = YANGDynClass(base=YANGBool, default=YANGBool("false"), is_leaf=True, yang_name="receive", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='boolean', is_config=False)


  def _get_send_max(self):
    """
    Getter method for send_max, mapped from YANG variable /bgp/neighbors/neighbor/add_paths/state/send_max (uint8)

    YANG Description: The maximum number of paths to advertise to neighbors
for a single NLRI
    """
    return self.__send_max
      
  def _set_send_max(self, v, load=False):
    """
    Setter method for send_max, mapped from YANG variable /bgp/neighbors/neighbor/add_paths/state/send_max (uint8)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_send_max is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_send_max() directly.

    YANG Description: The maximum number of paths to advertise to neighbors
for a single NLRI
    """
    try:
      t = YANGDynClass(v,base=RestrictedClassType(base_type=int, restriction_dict={'range': ['0..255']}, int_size=8), is_leaf=True, yang_name="send-max", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint8', is_config=False)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """send_max must be of a type compatible with uint8""",
          'defined-type': "uint8",
          'generated-type': """YANGDynClass(base=RestrictedClassType(base_type=int, restriction_dict={'range': ['0..255']}, int_size=8), is_leaf=True, yang_name="send-max", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint8', is_config=False)""",
        })

    self.__send_max = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_send_max(self):
    self.__send_max = YANGDynClass(base=RestrictedClassType(base_type=int, restriction_dict={'range': ['0..255']}, int_size=8), is_leaf=True, yang_name="send-max", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint8', is_config=False)

  receive = property(_get_receive)
  send_max = property(_get_send_max)


  _pyangbind_elements = {'receive': receive, 'send_max': send_max, }


