
from operator import attrgetter
import pyangbind.lib.xpathhelper as xpathhelper
from pyangbind.lib.yangtypes import RestrictedPrecisionDecimalType, RestrictedClassType, TypedListType
from pyangbind.lib.yangtypes import YANGBool, YANGListType, YANGDynClass, ReferenceType
from pyangbind.lib.base import PybindBase
from decimal import Decimal
from bitarray import bitarray
import config
import state
import prefixes
class prefix_set(PybindBase):
  """
  This class was auto-generated by the PythonClass plugin for PYANG
  from YANG module openconfig-routing-policy - based on the path /routing-policy/defined-sets/prefix-sets/prefix-set. Each member element of
  the container is represented as a class variable - with a specific
  YANG type.

  YANG Description: List of the defined prefix sets
  """
  __slots__ = ('_pybind_generated_by', '_path_helper', '_yang_name', '_extmethods', '__prefix_set_name','__config','__state','__prefixes',)

  _yang_name = 'prefix-set'

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
    self.__prefixes = YANGDynClass(base=prefixes.prefixes, is_container='container', yang_name="prefixes", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/routing-policy', defining_module='openconfig-routing-policy', yang_type='container', is_config=True)
    self.__state = YANGDynClass(base=state.state, is_container='container', yang_name="state", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/routing-policy', defining_module='openconfig-routing-policy', yang_type='container', is_config=True)
    self.__config = YANGDynClass(base=config.config, is_container='container', yang_name="config", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/routing-policy', defining_module='openconfig-routing-policy', yang_type='container', is_config=True)
    self.__prefix_set_name = YANGDynClass(base=ReferenceType(referenced_path='../config/prefix-set-name', caller=self._path() + ['prefix-set-name'], path_helper=self._path_helper, require_instance=True), is_leaf=True, yang_name="prefix-set-name", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, is_keyval=True, namespace='http://openconfig.net/yang/routing-policy', defining_module='openconfig-routing-policy', yang_type='leafref', is_config=True)

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
      return [u'routing-policy', u'defined-sets', u'prefix-sets', u'prefix-set']

  def _get_prefix_set_name(self):
    """
    Getter method for prefix_set_name, mapped from YANG variable /routing_policy/defined_sets/prefix_sets/prefix_set/prefix_set_name (leafref)

    YANG Description: Reference to prefix name list key
    """
    return self.__prefix_set_name
      
  def _set_prefix_set_name(self, v, load=False):
    """
    Setter method for prefix_set_name, mapped from YANG variable /routing_policy/defined_sets/prefix_sets/prefix_set/prefix_set_name (leafref)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_prefix_set_name is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_prefix_set_name() directly.

    YANG Description: Reference to prefix name list key
    """
    parent = getattr(self, "_parent", None)
    if parent is not None and load is False:
      raise AttributeError("Cannot set keys directly when" +
                             " within an instantiated list")

    try:
      t = YANGDynClass(v,base=ReferenceType(referenced_path='../config/prefix-set-name', caller=self._path() + ['prefix-set-name'], path_helper=self._path_helper, require_instance=True), is_leaf=True, yang_name="prefix-set-name", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, is_keyval=True, namespace='http://openconfig.net/yang/routing-policy', defining_module='openconfig-routing-policy', yang_type='leafref', is_config=True)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """prefix_set_name must be of a type compatible with leafref""",
          'defined-type': "leafref",
          'generated-type': """YANGDynClass(base=ReferenceType(referenced_path='../config/prefix-set-name', caller=self._path() + ['prefix-set-name'], path_helper=self._path_helper, require_instance=True), is_leaf=True, yang_name="prefix-set-name", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, is_keyval=True, namespace='http://openconfig.net/yang/routing-policy', defining_module='openconfig-routing-policy', yang_type='leafref', is_config=True)""",
        })

    self.__prefix_set_name = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_prefix_set_name(self):
    self.__prefix_set_name = YANGDynClass(base=ReferenceType(referenced_path='../config/prefix-set-name', caller=self._path() + ['prefix-set-name'], path_helper=self._path_helper, require_instance=True), is_leaf=True, yang_name="prefix-set-name", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, is_keyval=True, namespace='http://openconfig.net/yang/routing-policy', defining_module='openconfig-routing-policy', yang_type='leafref', is_config=True)


  def _get_config(self):
    """
    Getter method for config, mapped from YANG variable /routing_policy/defined_sets/prefix_sets/prefix_set/config (container)

    YANG Description: Configuration data for prefix sets
    """
    return self.__config
      
  def _set_config(self, v, load=False):
    """
    Setter method for config, mapped from YANG variable /routing_policy/defined_sets/prefix_sets/prefix_set/config (container)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_config is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_config() directly.

    YANG Description: Configuration data for prefix sets
    """
    try:
      t = YANGDynClass(v,base=config.config, is_container='container', yang_name="config", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/routing-policy', defining_module='openconfig-routing-policy', yang_type='container', is_config=True)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """config must be of a type compatible with container""",
          'defined-type': "container",
          'generated-type': """YANGDynClass(base=config.config, is_container='container', yang_name="config", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/routing-policy', defining_module='openconfig-routing-policy', yang_type='container', is_config=True)""",
        })

    self.__config = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_config(self):
    self.__config = YANGDynClass(base=config.config, is_container='container', yang_name="config", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/routing-policy', defining_module='openconfig-routing-policy', yang_type='container', is_config=True)


  def _get_state(self):
    """
    Getter method for state, mapped from YANG variable /routing_policy/defined_sets/prefix_sets/prefix_set/state (container)

    YANG Description: Operational state data 
    """
    return self.__state
      
  def _set_state(self, v, load=False):
    """
    Setter method for state, mapped from YANG variable /routing_policy/defined_sets/prefix_sets/prefix_set/state (container)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_state is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_state() directly.

    YANG Description: Operational state data 
    """
    try:
      t = YANGDynClass(v,base=state.state, is_container='container', yang_name="state", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/routing-policy', defining_module='openconfig-routing-policy', yang_type='container', is_config=True)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """state must be of a type compatible with container""",
          'defined-type': "container",
          'generated-type': """YANGDynClass(base=state.state, is_container='container', yang_name="state", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/routing-policy', defining_module='openconfig-routing-policy', yang_type='container', is_config=True)""",
        })

    self.__state = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_state(self):
    self.__state = YANGDynClass(base=state.state, is_container='container', yang_name="state", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/routing-policy', defining_module='openconfig-routing-policy', yang_type='container', is_config=True)


  def _get_prefixes(self):
    """
    Getter method for prefixes, mapped from YANG variable /routing_policy/defined_sets/prefix_sets/prefix_set/prefixes (container)

    YANG Description: Enclosing container for the list of prefixes in a policy
prefix list
    """
    return self.__prefixes
      
  def _set_prefixes(self, v, load=False):
    """
    Setter method for prefixes, mapped from YANG variable /routing_policy/defined_sets/prefix_sets/prefix_set/prefixes (container)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_prefixes is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_prefixes() directly.

    YANG Description: Enclosing container for the list of prefixes in a policy
prefix list
    """
    try:
      t = YANGDynClass(v,base=prefixes.prefixes, is_container='container', yang_name="prefixes", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/routing-policy', defining_module='openconfig-routing-policy', yang_type='container', is_config=True)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """prefixes must be of a type compatible with container""",
          'defined-type': "container",
          'generated-type': """YANGDynClass(base=prefixes.prefixes, is_container='container', yang_name="prefixes", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/routing-policy', defining_module='openconfig-routing-policy', yang_type='container', is_config=True)""",
        })

    self.__prefixes = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_prefixes(self):
    self.__prefixes = YANGDynClass(base=prefixes.prefixes, is_container='container', yang_name="prefixes", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/routing-policy', defining_module='openconfig-routing-policy', yang_type='container', is_config=True)

  prefix_set_name = property(_get_prefix_set_name, _set_prefix_set_name)
  config = property(_get_config, _set_config)
  state = property(_get_state, _set_state)
  prefixes = property(_get_prefixes, _set_prefixes)


  _pyangbind_elements = {'prefix_set_name': prefix_set_name, 'config': config, 'state': state, 'prefixes': prefixes, }


