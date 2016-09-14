
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
  from YANG module openconfig-bgp - based on the path /bgp/peer-groups/peer-group/graceful-restart/state. Each member element of
  the container is represented as a class variable - with a specific
  YANG type.

  YANG Description: State information associated with graceful-restart
  """
  __slots__ = ('_pybind_generated_by', '_path_helper', '_yang_name', '_extmethods', '__enabled','__restart_time','__stale_routes_time','__helper_only',)

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
    self.__stale_routes_time = YANGDynClass(base=RestrictedPrecisionDecimalType(precision=2), is_leaf=True, yang_name="stale-routes-time", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='decimal64', is_config=False)
    self.__restart_time = YANGDynClass(base=RestrictedClassType(base_type=RestrictedClassType(base_type=int, restriction_dict={'range': ['0..65535']},int_size=16), restriction_dict={'range': [u'0..4096']}), is_leaf=True, yang_name="restart-time", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint16', is_config=False)
    self.__enabled = YANGDynClass(base=YANGBool, is_leaf=True, yang_name="enabled", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='boolean', is_config=False)
    self.__helper_only = YANGDynClass(base=YANGBool, is_leaf=True, yang_name="helper-only", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='boolean', is_config=False)

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
      return [u'bgp', u'peer-groups', u'peer-group', u'graceful-restart', u'state']

  def _get_enabled(self):
    """
    Getter method for enabled, mapped from YANG variable /bgp/peer_groups/peer_group/graceful_restart/state/enabled (boolean)

    YANG Description: Enable or disable the graceful-restart capability.
    """
    return self.__enabled
      
  def _set_enabled(self, v, load=False):
    """
    Setter method for enabled, mapped from YANG variable /bgp/peer_groups/peer_group/graceful_restart/state/enabled (boolean)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_enabled is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_enabled() directly.

    YANG Description: Enable or disable the graceful-restart capability.
    """
    try:
      t = YANGDynClass(v,base=YANGBool, is_leaf=True, yang_name="enabled", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='boolean', is_config=False)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """enabled must be of a type compatible with boolean""",
          'defined-type': "boolean",
          'generated-type': """YANGDynClass(base=YANGBool, is_leaf=True, yang_name="enabled", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='boolean', is_config=False)""",
        })

    self.__enabled = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_enabled(self):
    self.__enabled = YANGDynClass(base=YANGBool, is_leaf=True, yang_name="enabled", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='boolean', is_config=False)


  def _get_restart_time(self):
    """
    Getter method for restart_time, mapped from YANG variable /bgp/peer_groups/peer_group/graceful_restart/state/restart_time (uint16)

    YANG Description: Estimated time (in seconds) for the local BGP speaker to
restart a session. This value is advertise in the graceful
restart BGP capability.  This is a 12-bit value, referred to
as Restart Time in RFC4724.  Per RFC4724, the suggested
default value is <= the hold-time value.
    """
    return self.__restart_time
      
  def _set_restart_time(self, v, load=False):
    """
    Setter method for restart_time, mapped from YANG variable /bgp/peer_groups/peer_group/graceful_restart/state/restart_time (uint16)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_restart_time is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_restart_time() directly.

    YANG Description: Estimated time (in seconds) for the local BGP speaker to
restart a session. This value is advertise in the graceful
restart BGP capability.  This is a 12-bit value, referred to
as Restart Time in RFC4724.  Per RFC4724, the suggested
default value is <= the hold-time value.
    """
    try:
      t = YANGDynClass(v,base=RestrictedClassType(base_type=RestrictedClassType(base_type=int, restriction_dict={'range': ['0..65535']},int_size=16), restriction_dict={'range': [u'0..4096']}), is_leaf=True, yang_name="restart-time", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint16', is_config=False)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """restart_time must be of a type compatible with uint16""",
          'defined-type': "uint16",
          'generated-type': """YANGDynClass(base=RestrictedClassType(base_type=RestrictedClassType(base_type=int, restriction_dict={'range': ['0..65535']},int_size=16), restriction_dict={'range': [u'0..4096']}), is_leaf=True, yang_name="restart-time", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint16', is_config=False)""",
        })

    self.__restart_time = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_restart_time(self):
    self.__restart_time = YANGDynClass(base=RestrictedClassType(base_type=RestrictedClassType(base_type=int, restriction_dict={'range': ['0..65535']},int_size=16), restriction_dict={'range': [u'0..4096']}), is_leaf=True, yang_name="restart-time", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint16', is_config=False)


  def _get_stale_routes_time(self):
    """
    Getter method for stale_routes_time, mapped from YANG variable /bgp/peer_groups/peer_group/graceful_restart/state/stale_routes_time (decimal64)

    YANG Description: An upper-bound on the time thate stale routes will be
retained by a router after a session is restarted. If an
End-of-RIB (EOR) marker is received prior to this timer
expiring stale-routes will be flushed upon its receipt - if
no EOR is received, then when this timer expires stale paths
will be purged. This timer is referred to as the
Selection_Deferral_Timer in RFC4724
    """
    return self.__stale_routes_time
      
  def _set_stale_routes_time(self, v, load=False):
    """
    Setter method for stale_routes_time, mapped from YANG variable /bgp/peer_groups/peer_group/graceful_restart/state/stale_routes_time (decimal64)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_stale_routes_time is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_stale_routes_time() directly.

    YANG Description: An upper-bound on the time thate stale routes will be
retained by a router after a session is restarted. If an
End-of-RIB (EOR) marker is received prior to this timer
expiring stale-routes will be flushed upon its receipt - if
no EOR is received, then when this timer expires stale paths
will be purged. This timer is referred to as the
Selection_Deferral_Timer in RFC4724
    """
    try:
      t = YANGDynClass(v,base=RestrictedPrecisionDecimalType(precision=2), is_leaf=True, yang_name="stale-routes-time", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='decimal64', is_config=False)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """stale_routes_time must be of a type compatible with decimal64""",
          'defined-type': "decimal64",
          'generated-type': """YANGDynClass(base=RestrictedPrecisionDecimalType(precision=2), is_leaf=True, yang_name="stale-routes-time", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='decimal64', is_config=False)""",
        })

    self.__stale_routes_time = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_stale_routes_time(self):
    self.__stale_routes_time = YANGDynClass(base=RestrictedPrecisionDecimalType(precision=2), is_leaf=True, yang_name="stale-routes-time", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='decimal64', is_config=False)


  def _get_helper_only(self):
    """
    Getter method for helper_only, mapped from YANG variable /bgp/peer_groups/peer_group/graceful_restart/state/helper_only (boolean)

    YANG Description: Enable graceful-restart in helper mode only. When this
leaf is set, the local system does not retain forwarding
its own state during a restart, but supports procedures
for the receiving speaker, as defined in RFC4724.
    """
    return self.__helper_only
      
  def _set_helper_only(self, v, load=False):
    """
    Setter method for helper_only, mapped from YANG variable /bgp/peer_groups/peer_group/graceful_restart/state/helper_only (boolean)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_helper_only is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_helper_only() directly.

    YANG Description: Enable graceful-restart in helper mode only. When this
leaf is set, the local system does not retain forwarding
its own state during a restart, but supports procedures
for the receiving speaker, as defined in RFC4724.
    """
    try:
      t = YANGDynClass(v,base=YANGBool, is_leaf=True, yang_name="helper-only", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='boolean', is_config=False)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """helper_only must be of a type compatible with boolean""",
          'defined-type': "boolean",
          'generated-type': """YANGDynClass(base=YANGBool, is_leaf=True, yang_name="helper-only", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='boolean', is_config=False)""",
        })

    self.__helper_only = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_helper_only(self):
    self.__helper_only = YANGDynClass(base=YANGBool, is_leaf=True, yang_name="helper-only", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='boolean', is_config=False)

  enabled = property(_get_enabled)
  restart_time = property(_get_restart_time)
  stale_routes_time = property(_get_stale_routes_time)
  helper_only = property(_get_helper_only)


  _pyangbind_elements = {'enabled': enabled, 'restart_time': restart_time, 'stale_routes_time': stale_routes_time, 'helper_only': helper_only, }


