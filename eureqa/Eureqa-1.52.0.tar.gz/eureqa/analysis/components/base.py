# Copyright (c) 2016, Nutonian Inc
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the Nutonian Inc nor the
#     names of its contributors may be used to endorse or promote products
#     derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL NUTONIAN INC BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import uuid
from eureqa.utils.jsonrest import _JsonREST

# Python Metaclass that automatically tracks all known types of Components
# If you're in this file, you probably want to skip ahead to 'class Component()' below.
# The following code has a very specific use case.
class _ComponentRegistrar(type):
    """ For internal use only. """

    # For those not familiar with Python metaclasses and __new__:
    #
    # __init__() runs when an *instance* is created.
    # __new__() runs when a *class* is created.
    #
    # In the common case (unless you're creating classes on the fly), a class
    # is "constructed" in this sense when Python first opens and parses the
    # file containing this class.
    #
    # The "Component" class represents a common base class for a
    # collection of serializable objects.
    # The serialized representation of the class contains a 'type' string
    # that indicates what type of thing has been serialized; therefore,
    # which Python class should be used to represent it.
    # In order to de-serialize such objects, 'Component' must therefore
    # know about all of its subclasses that represent specific
    # types of objects, as well as which class represents which 'type'
    # string.
    # Rather than write and maintain a list, this code makes the Python
    # interpreter generate the list for us.

    def __new__(type_, name, bases, dict_):
        cls = type.__new__(type_, name, bases, dict_)
        assert hasattr(cls, "_component_type_str"), \
            "New Analysis Component classes must define a '_component_type' field"
        cls._register(cls._component_type_str)
        return cls


class _Component(_JsonREST):
    """
    Component base class.
    Implements common logic shared by all components.
    Do not construct this class directly; instead,
    construct the specific component that you want.

    Notes for component implementors:  (If your new class's sub-Components aren't showing up properly, read on!)

    The backend first sees a Component when the first of the following happens:
      * The Component is constructed with an Analysis passed into the constructor as an argument
      * The Component is added to an Item that is already attached to an Analysis
      * The Component is added to an Item that is not already attached to an Analysis, and then the Item is attached to an Analysis
      * The Component is added to a Table and that Table's data is uploaded
    If more than one of these things happens in the lifecycle of a Component, or if one happens repeatedly,
    only the very first occurrence counts.
    Call this first event "Association".

    Before Association, each individual Component subclass is responsible for tracking their sub-Components (if any).
    At Association, "Component._associate()" is called; each Component that holds sub-Components must override this
    method to also call "_associate()" on all of their sub-Components.
    After Association (and *NOT* before it), each Component is responsible for immediately calling "_associate()"
    on any sub-Component that is added to it.
    """

    __metaclass__ = _ComponentRegistrar

    def clone(self):
        # Make a copy of ourselves
        body = self._to_json()

        # Disassociate the copy from the current Analysis
        if "analysis_id" in body:
            del body["analysis_id"]
        if "component_id" in body:
            del body["component_id"]

        # Instantiate a new Item with this state
        return _Component._construct_from_json(body)

    def delete(self):
        """ Remove this Component from the server. """
        # Subclasses may override this to do more elaborate clean-up.
        self._delete()

    def __init__(self, _analysis=None, _component_id=None, _component_type=None):
        """ For internal use only. """
        if _component_id is not None:
            self._component_id = _component_id

        if _component_type is not None:
            self._component_type = _component_type
        else:
            self._component_type = self._component_type_str

        if _analysis:
            self._associate(_analysis)

    _component_type_str = "GENERIC_COMPONENT"
    _registered_types = {}

    @classmethod
    def _register(cls, component_type):
        cls._registered_types[component_type] = cls

    def _populate_eureqa(self):
        if not hasattr(self, "_analysis"):
            # Can't populate Eureqa yet
            return

        self._eureqa = self._analysis._eureqa


    # Override "_construct_from_json()" to use the appropriate subclass if possible
    @classmethod
    def _construct_from_json(cls, body, *args, **kwargs):

        # If we're given an analysis, pass it in after
        # we're done populating the object so that we don't make
        # extraneous HTTP requests populating partial object state.
        analysis = None
        if "_analysis" in kwargs:
            analysis = kwargs["_analysis"]
            del kwargs["_analysis"]

        ret = cls._registered_types.get(body.get("component_type"), _Component)(*args, **kwargs)
        ret._from_json(body)

        if analysis is not None:
            ret._associate(analysis)

        ret._populate_eureqa()
        return ret

    # Override "_get_all_from_self()" to associate all newly-constructed components
    # with our Analysis (if any)
    def _get_all_from_self(self):
        """
        Fetch a list of all objects in the same directory as this object.
        :return: list() of objects of the current type
        """
        comps = super(_Component, self)._get_all_from_self()

        if hasattr(self, "_analysis"):
            for comp in comps:
                comp._associate(self._analysis)

        return comps

    def _object_endpoint(self):
        return '/analysis/%s/components/%s' % (self._analysis._id, self._component_id)

    def _directory_endpoint(self):
        return '/analysis/%s/components' % (self._analysis._id)

    def _fields(self):
        return [ "analysis_id", "component_id", "component_type" ]

    def _to_json(self):
        resp = super(_Component, self)._to_json()

        if hasattr(self, "_analysis"):
            resp["analysis_id"] = self._analysis._id

        return resp

    def _from_json(self, body):
        if hasattr(self, "_analysis") and body.get("analysis_id"):
            assert body.get("analysis_id") == self._analysis._id, \
                "_from_json() can't de-serialize an Item that belongs to a different Analysis"

        super(_Component, self)._from_json(body)

    def _associate(self, analysis):
        self._analysis = analysis
        self._analysis_id = analysis._id
        _JsonREST.__init__(self, analysis._eureqa)
        self._populate_eureqa()
        if not hasattr(self, "_component_id"):
            # Get an ID and whatnot only if we don't already have one.
            self._create()

    def _associate_with_table(self, analysis):
        # The base class implementation of this method only generates UUID but
        # does not add them to the actual analysis. Because most components
        # are directly inlined into the table and some involve extra actions (e.g. uploading a file)
        # It is up to a particular component to override this method and provide more
        # specific implementation.
        if not hasattr(self, "_component_id"):
            self._component_id = str(uuid.uuid4())
        return [self._to_json()]

class _TwoVariablePlotComponent(_Component):
    _component_type_str = "TwoVariablePlot helper mixin (not a complete type)"


    def __init__(self, _analysis=None, _component_id=None, _component_type=None):

        super(_TwoVariablePlotComponent, self).__init__(_analysis=_analysis, _component_id=_component_id, _component_type=_component_type)

        default_x_label = getattr(self, '_x_var', 'the x var')
        default_y_label = getattr(self, '_y_var', 'the y var')

        DEFAULTS = {'BOX_PLOT':             {'default_label' : { 'x': default_x_label, 'y': default_y_label },
                                             'default_format': { 'x': 'g',   'y': '.2s' }},

                    'DOUBLE_HISTOGRAM_PLOT':{'default_label' : { 'x': [default_x_label, default_y_label], 'y': 'number of values' },
                                             'default_format': { 'x': 'g', 'y': '.3s' }},

                    'SCATTER_PLOT':         {'default_label' : { 'x': default_x_label, 'y': default_y_label },
                                             'default_format': { 'x': '.3s', 'y': '.3s' }},

                    'BINNED_MEAN_PLOT':     {'default_label' : { 'x': default_x_label, 'y': default_y_label },
                                             'default_format': { 'x': '.3s', 'y': '.2f' }}}



        default_values = DEFAULTS.get(self._component_type,
                                      {'default_label' : { 'x': default_x_label, 'y': default_y_label },
                                       'default_format': { 'x': '.3s', 'y': '.3s' }})

        if not hasattr(self,'_axisLabels'):
            self._axisLabels = default_values['default_label']
        if not hasattr(self,'_labelFormat'):
            self._labelFormat = default_values['default_format']


    class XYMap(object):
        """ A named tuple with keys 'x' and 'y'

        :param TwoVariablePlotCard tvp: The TwoVariablePlotCard object.
        :param dict dic: X and Y parameters as dictionary.
        """

        def __init__(self, parent_component, body):
            self._parent_component = parent_component
            self._body = body

        @property
        def x(self):
            """ X value """
            return self._body['x']

        @x.setter
        def x(self, val):
            self._body['x'] = val
            self._update()

        @property
        def y(self):
            """ Y value """
            return self._body['y']

        @y.setter
        def y(self, val):
            self._body['y'] = val
            self._update()

        def _update(self):
            self._parent_component._update()
