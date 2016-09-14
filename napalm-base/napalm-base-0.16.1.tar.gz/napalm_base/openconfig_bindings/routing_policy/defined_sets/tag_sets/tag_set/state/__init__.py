
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
  from YANG module openconfig-routing-policy - based on the path /routing-policy/defined-sets/tag-sets/tag-set/state. Each member element of
  the container is represented as a class variable - with a specific
  YANG type.

  YANG Description: Operational state data for tag sets
  """
  __slots__ = ('_pybind_generated_by', '_path_helper', '_yang_name', '_extmethods', '__tag_set_name','__tag_value',)

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
    self.__tag_set_name = YANGDynClass(base=unicode, is_leaf=True, yang_name="tag-set-name", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/routing-policy', defining_module='openconfig-routing-policy', yang_type='string', is_config=False)
    self.__tag_value = YANGDynClass(base=TypedListType(allowed_type=[RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32),RestrictedClassType(base_type=unicode, restriction_dict={'pattern': u'([0-9a-fA-F]{2}(:[0-9a-fA-F]{2})*)?'}),]), is_leaf=False, yang_name="tag-value", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/routing-policy', defining_module='openconfig-routing-policy', yang_type='oc-pol-types:tag-type', is_config=False)

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
      return [u'routing-policy', u'defined-sets', u'tag-sets', u'tag-set', u'state']

  def _get_tag_set_name(self):
    """
    Getter method for tag_set_name, mapped from YANG variable /routing_policy/defined_sets/tag_sets/tag_set/state/tag_set_name (string)

    YANG Description: name / label of the tag set -- this is used to reference
the set in match conditions
    """
    return self.__tag_set_name
      
  def _set_tag_set_name(self, v, load=False):
    """
    Setter method for tag_set_name, mapped from YANG variable /routing_policy/defined_sets/tag_sets/tag_set/state/tag_set_name (string)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_tag_set_name is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_tag_set_name() directly.

    YANG Description: name / label of the tag set -- this is used to reference
the set in match conditions
    """
    try:
      t = YANGDynClass(v,base=unicode, is_leaf=True, yang_name="tag-set-name", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/routing-policy', defining_module='openconfig-routing-policy', yang_type='string', is_config=False)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """tag_set_name must be of a type compatible with string""",
          'defined-type': "string",
          'generated-type': """YANGDynClass(base=unicode, is_leaf=True, yang_name="tag-set-name", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/routing-policy', defining_module='openconfig-routing-policy', yang_type='string', is_config=False)""",
        })

    self.__tag_set_name = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_tag_set_name(self):
    self.__tag_set_name = YANGDynClass(base=unicode, is_leaf=True, yang_name="tag-set-name", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/routing-policy', defining_module='openconfig-routing-policy', yang_type='string', is_config=False)


  def _get_tag_value(self):
    """
    Getter method for tag_value, mapped from YANG variable /routing_policy/defined_sets/tag_sets/tag_set/state/tag_value (oc-pol-types:tag-type)

    YANG Description: Value of the tag set member
    """
    return self.__tag_value
      
  def _set_tag_value(self, v, load=False):
    """
    Setter method for tag_value, mapped from YANG variable /routing_policy/defined_sets/tag_sets/tag_set/state/tag_value (oc-pol-types:tag-type)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_tag_value is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_tag_value() directly.

    YANG Description: Value of the tag set member
    """
    try:
      t = YANGDynClass(v,base=TypedListType(allowed_type=[RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32),RestrictedClassType(base_type=unicode, restriction_dict={'pattern': u'([0-9a-fA-F]{2}(:[0-9a-fA-F]{2})*)?'}),]), is_leaf=False, yang_name="tag-value", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/routing-policy', defining_module='openconfig-routing-policy', yang_type='oc-pol-types:tag-type', is_config=False)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """tag_value must be of a type compatible with oc-pol-types:tag-type""",
          'defined-type': "oc-pol-types:tag-type",
          'generated-type': """YANGDynClass(base=TypedListType(allowed_type=[RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32),RestrictedClassType(base_type=unicode, restriction_dict={'pattern': u'([0-9a-fA-F]{2}(:[0-9a-fA-F]{2})*)?'}),]), is_leaf=False, yang_name="tag-value", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/routing-policy', defining_module='openconfig-routing-policy', yang_type='oc-pol-types:tag-type', is_config=False)""",
        })

    self.__tag_value = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_tag_value(self):
    self.__tag_value = YANGDynClass(base=TypedListType(allowed_type=[RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32),RestrictedClassType(base_type=unicode, restriction_dict={'pattern': u'([0-9a-fA-F]{2}(:[0-9a-fA-F]{2})*)?'}),]), is_leaf=False, yang_name="tag-value", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/routing-policy', defining_module='openconfig-routing-policy', yang_type='oc-pol-types:tag-type', is_config=False)

  tag_set_name = property(_get_tag_set_name)
  tag_value = property(_get_tag_value)


  _pyangbind_elements = {'tag_set_name': tag_set_name, 'tag_value': tag_value, }


