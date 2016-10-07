from builtins import super

import ctypes
import logging
import re

from collections import namedtuple
from fnmatch import fnmatch
from functools import reduce
from keyword import iskeyword
from six import string_types
from textwrap import dedent

from ..tecutil import (_tecutil, ArgList, Index, IndexSet, flatten_args,
                       log_setattr)
from .. import layout
from ..constant import *
from ..exception import *
from ..tecutil import lock
from ..tecutil import sv

log = logging.getLogger(__name__)


# noinspection PyShadowingNames
@log_setattr
class Array(ctypes.c_void_p):
    """Low-level accessor for underlying data within a `Dataset`."""
    def __init__(self, dataset, zone, variable):
        self.dataset = dataset
        self.zone = zone
        self.variable = variable
        super().__init__(self._native_reference)

    @property
    @lock()
    def _native_reference(self):
        return _tecutil.DataValueGetReadableNativeRefByUniqueID(
            self.dataset.uid, self.zone.index+1, self.variable.index+1)

    def __eq__(self, other):
        return ctypes.addressof(self) == ctypes.addressof(other)

    def __len__(self):
        return self.shape[0]

    @property
    def size(self):
        return _tecutil.DataValueGetCountByRef(self)

    @property
    def shape(self):
        """(i,j,k) shape"""
        return self.zone.shape

    @property
    def c_type(self):
        _ctypes = {
            FieldDataType.Float: ctypes.c_float,
            FieldDataType.Double: ctypes.c_double,
            FieldDataType.Int32: ctypes.c_int,
            FieldDataType.Int16: ctypes.c_int16,
            FieldDataType.Byte: ctypes.c_int8}
        return _ctypes[self.data_type]

    @property
    def data_type(self):
        return _tecutil.DataValueGetRefType(self)

    @property
    def data(self):
        _tecutil.handle.tecUtilDataValueGetWritableRawPtrByRef.restype = \
            ctypes.POINTER(self.c_type)
        return _tecutil.DataValueGetWritableRawPtrByRef(self)

    @lock()
    def copy(self, offset=0, size=None):
        size = self.size if size is None else size
        arr = (self.c_type * size)()
        _tecutil.DataValueArrayGetByRef(self, offset+1, size, arr)
        return arr

    def _slice_range(self, s):
        start = s.start or 0
        stop = s.stop or self.size
        step = s.step or 1
        return range(start, stop, step)

    def __getitem__(self, i):
        if isinstance(i, slice):
            data = self.data
            return [data[ii] for ii in self._slice_range(i)]
        else:
            return self.data[i]

    def __setitem__(self, i, val):
        if isinstance(i, slice):
            data = self.data
            for ii in self._slice_range(i):
                data[ii] = val[ii]
        else:
            self.data[i] = val

    def __iter__(self):
        self.current_index = -1
        self.current_length = self.size
        return self

    def __next__(self):
        self.current_index += 1
        if self.current_index < self.current_length:
            return self.__getitem__(self.current_index)
        else:
            del self.current_index
            del self.current_length
            raise StopIteration()

    @property
    def minmax(self):
        return _tecutil.DataValueGetMinMaxByRef(self)

    def min(self):
        return self.minmax[0]

    def max(self):
        return self.minmax[1]


# noinspection PyShadowingNames
@log_setattr
class Zone(object):
    """Key value for a data array within a `Dataset`.

    Parameters:
        uid (`integer <int>`): This must be a *valid* unique ID number
            pointing internally to a `Zone` object in the given `Dataset`.
        dataset (`Dataset`): A `Dataset` to which this `Zone` is contained.

    `Zones <Zone>` can be identified (uniquely) by the index with their
    parent `Dataset` or (non-uniquely) by name. In general, a `Variable`
    must be selected to access the underlying data array.
    """
    def __init__(self, uid, dataset):
        self.uid = uid
        self.dataset = dataset

    # string representations
    def __str__(self):
        """Brief string representation.

        Returns:
            `string <str>`: Brief representation of this `Zone`, showing a list
            of associated `Variables <Variable>`.

        Example::

            >>> rect_zone = dataset.zone('Rectangular zone')
            >>> print(rect_zone)
            Zone: Rectangular zone
              Variables: ['x', 'y', 'z']
        """
        fmt = 'Zone: {}\n  Variables: [{}]'
        vnames = ["'{}'".format(v.name) for v in self.dataset.variables()]
        return fmt.format(self.name, ','.join(vnames))

    def __repr__(self):
        """Executable string representation.

        Returns:
            `string <str>`: Internal representation of this `Zone`.

        The string returned can be executed to generate a clone of this
        `Zone` object::

            >>> rectzone = dataset.zone('Rectangular zone')
            >>> print(repr(rectzone))
            Zone(uid=31, Dataset(uid=21, frame=Frame(uid=11, page=Page(uid=1)))
            >>> exec('rectzone_clone = '+repr(rectzone))
            >>> rectzone_clone
            Zone(uid=31, Dataset(uid=21, frame=Frame(uid=11, page=Page(uid=1)))
            >>> rectzone == rectzone_clone
            True
        """
        return 'Zone(uid={uid}, dataset={dataset})'.format(
            uid=self.uid, dataset=repr(self.dataset))

    def __eq__(self, other):
        """Checks for equality in the |Tecplot Engine|.

        Returns:
            `bool`: `True` if the unique ID numbers are the same for both
            `Zones <Zone>`.
        """
        return self.uid == other.uid

    @property
    def index(self):
        """Zero-based position within the parent `Dataset`.

        :type: `Index`
        """
        return Index(_tecutil.ZoneGetNumByUniqueID(self.uid)-1)

    @property
    def strand(self):
        """Returns the StrandID.

        :type: `Index`
        """
        return Index(_tecutil.ZoneGetStrandID(self.index+1)-1)

    @strand.setter
    @lock()
    def strand(self, value):
        _tecutil.ZoneSetStrandID(self.index+1, value+1)

    @property
    def solution_time(self):
        """Returns the solution time.

        :type: `float`
        """
        return _tecutil.ZoneGetSolutionTime(self.index+1)

    @solution_time.setter
    @lock()
    def solution_time(self, value):
        _tecutil.ZoneSetSolutionTime(self.index+1, value)

    @property
    def type(self):
        """Returns the zone type.

        :type: `ZoneType`
        """
        return _tecutil.ZoneGetType(self.index+1)

    @property
    def name(self):
        """Returns or sets the name.

        :type: `string <str>`

        Raises:
            `TecplotSystemError`
        """
        res, zname = _tecutil.ZoneGetNameByDataSetID(self.dataset.uid,
                                                     self.index+1)
        if not res:
            TecplotSystemError()
        return zname

    @name.setter
    @lock()
    def name(self, name):
        _tecutil.ZoneRenameByDataSetID(self.dataset.uid, self.index+1, name)

    @property
    def num_variables(self):
        """Number of `Variables <Variable>` in the parent `Dataset`.

        :type: `integer <int>`
        """
        return self.dataset.num_variables

    def variable(self, pattern):
        """Returns an `Array` by index or string pattern.

        Parameters:
            pattern (`integer <int>` or `string <str>`):  Zero-based index or
                `glob-style pattern <fnmatch.fnmatch>` in which case, the
                first match is returned.

        The `Variable.name` attribute is used to match the *pattern* to the
        desired `Array` though this is not necessarily unique::

            >>> ds = frame.dataset
            >>> print(ds)
            Dataset:
              Zones: ['Rectangular zone']
              Variables: ['x', 'y', 'z']
            >>> zone = ds.zone('Rectangular zone')
            >>> x = zone.variable('x')
            >>> x == zone.variable(0)
            True
        """
        return Array(self.dataset, self, self.dataset.variable(pattern))

    def variables(self, pattern=None):
        """Yields all `Arrays <Array>` matching a *pattern*."""
        for variable in self.dataset.variables(pattern):
            yield Array(self.dataset, self, variable)

    def copy(self):
        """duplicate this `Zone` in its currently held parent `Dataset`."""
        return self.dataset.copy_zones(self)[0]

    @property
    def num_points(self):
        """Number of elements in the associated data array."""
        return reduce(lambda x, y: x*y,  self.shape, 1)

    @property
    def shape(self):
        """The shape of the associated data arrays.

        Returns:
            `tuple`(`int`): ``(i,j,k)`` for ordered data or ``(len,)`` for
            unordered data.
        """
        return _tecutil.ZoneGetIJKByUniqueID(self.dataset.uid, self.index+1)


# noinspection PyShadowingNames
@log_setattr
class Variable(object):
    """Key value for a data array within a `Dataset`.

    Parameters:
        uid (`integer <int>`): This must be a *valid* unique ID number
            pointing internally to a `Variable` object in the given `Dataset`.
        dataset (`Dataset`): A `Dataset` to which this `Variable` is contained.

    `Variables <Variable>` can be identified (uniquely) by the index with
    their parent `Dataset` or (non-uniquely) by name. In general, a `Zone`
    must be selected to access the underlying data array.
    """
    def __init__(self, uid, dataset):
        self.uid = uid
        self.dataset = dataset

    # string representations
    def __str__(self):
        """Brief string representation.

        Returns:
            `string <str>`: Brief representation of this `Variable`, showing
            `Zones <Zone>`.

        Example::

            >>> x = dataset.variable('x')
            >>> print(x)
            Variable: x
              Zones: ['Rectangular zone']
        """
        fmt = 'Variable: {}\n  Zones: [{}]'
        znames = ["'{}'".format(z.name) for z in self.dataset.zones()]
        return fmt.format(self.name, ','.join(znames))

    def __repr__(self):
        """Executable string representation.

        Returns:
            `string <str>`: Internal representation of this `Variable`.

        The string returned can be executed to generate a
        clone of this `Variable` object::

            >>> x = dataset.variable('x')
            >>> print(repr(x))
            Variable(uid=41, Dataset(uid=21, frame=Frame(uid=11,
            page=Page(uid=1)))
            >>> exec('x_clone = '+repr(x))
            >>> x_clone
            Variable(uid=41, Dataset(uid=21, frame=Frame(uid=11,
            page=Page(uid=1)))
            >>> x == x_clone
            True
        """
        return 'Variable(uid={uid}, dataset={dataset})'.format(
                uid=self.uid, dataset=repr(self.dataset))

    def __eq__(self, other):
        """Checks for equality in the |Tecplot Engine|.

        Returns:
            `bool`: `True` if the unique ID numbers are the same for both
            `Variables <Variable>`.
        """
        return self.uid == other.uid

    @property
    def index(self):
        """Zero-based position within the parent `Dataset`.

        :type: `Index`
        """
        return Index(_tecutil.VarGetNumByUniqueID(self.uid)-1)

    @property
    def name(self):
        """Returns or sets the name.

        :type: `string <str>`

        Raises:
            `TecplotSystemError`
        """
        res, var_name = _tecutil.VarGetNameByDataSetID(self.dataset.uid,
                                                       self.index+1)
        if not res:
            TecplotSystemError()
        return var_name

    @name.setter
    @lock()
    def name(self, name):
        _tecutil.VarRenameByDataSetID(self.dataset.uid, self.index+1, name)

    @property
    def num_zones(self):
        """Number of `Zones <Zone>` in the parent `Dataset`.

        :type: `integer <int>`
        """
        return self.dataset.num_zones

    def zone(self, pattern):
        """Returns `Array` by index or string pattern.

        Parameters:
            pattern (`integer <int>` or `string <str>`):  Zero-based index or
                `glob-style pattern <fnmatch.fnmatch>` in which case, the
                first match is returned.

        The `Zone.name` attribute is used to match the *pattern* to the desired
        `Array` though this is not necessarily unique::

            >>> ds = frame.dataset
            >>> print(ds)
            Dataset:
              Zones: ['Rectangular zone']
              Variables: ['x', 'y', 'z']
            >>> x = ds.variable('x')
            >>> rectzone = x.zone('Rectangular zone')
            >>> rectzone == x.zone(0)
            True
        """
        return Array(self.dataset, self.dataset.zone(pattern), self)

    def zones(self, pattern=None):
        """Yields all `Arrays <Array>` matching a *pattern*."""
        for zone in self.dataset.zones(pattern):
            yield Array(self.dataset, zone, self)


# noinspection PyShadowingNames
@log_setattr
class Dataset(object):
    """A matrix of `Zones <Zone>` and `Variables <Variable>`.

    Parameters:
        uid (`integer <int>`): This must be a *valid* unique ID number pointing
            internally to a `Dataset` object.
        frame (`Frame`): A `Frame` to which this `Dataset` is attached.

    A `Dataset` can be shared among several `Frames <Frame>`, though any
    particular `Dataset` object will have a handle to at least one of them.
    Any modification of a shared `Dataset` will be reflected in all
    `Frames <Frame>` that use it.
    """
    def __init__(self, uid, frame):
        self.uid = uid
        self.frame = frame

    def __repr__(self):
        """Executable string representation.

        Returns:
            `string <str>`: Internal representation of this `Dataset`.

        The string returned can be executed to generate a
        clone of this `Dataset` object::

            >>> dataset = frame.dataset
            >>> print(repr(dataset))
            Dataset(uid=21, frame=Frame(uid=11, page=Page(uid=1)))
            >>> exec('dataset_clone = '+repr(dataset))
            >>> dataset_clone
            Dataset(uid=21, frame=Frame(uid=11, page=Page(uid=1)))
            >>> dataset == dataset_clone
            True
        """
        return 'Dataset(uid={uid}, frame={frame})'.format(
            uid=self.uid, frame=repr(self.frame))

    def __str__(self):
        """Brief string representation.

        Returns:
            `string <str>`: Brief representation of this `Dataset`, showing
            `Zones <Zone>` and `Variables <Variable>`.

        Example::

            >>> dataset = frame.dataset
            >>> print(dataset)
            Dataset:
              Zones: ['Rectangular zone']
              Variables: ['x', 'y', 'z']
        """
        fmt = 'Dataset:\n  Zones: [{}]\n  Variables: [{}]'
        return fmt.format(
            ','.join("'{}'".format(z.name) for z in self.zones()),
            ','.join("'{}'".format(v.name) for v in self.variables()))

    def __eq__(self, other):
        """Checks for equality in the |Tecplot Engine|.

        Returns:
            `bool`: `True` if the unique ID numbers are the same for both
            `Datasets <Dataset>`.

        This can be useful for determining if two `Frames <Frame>`
        are holding on to the same `Dataset`::

            >>> frame1.dataset == frame2.dataset
            True
        """
        return self.uid == other.uid

    def __ne__(self, other):
        return not self.__eq__(other)

    def __contains__(self, obj):
        if obj.dataset == self:
            if isinstance(obj, Variable) and obj == self.variable(obj.index):
                return True
            elif isinstance(obj, Zone) and obj == self.zone(obj.index):
                return True
        return False

    @property
    def title(self):
        """Title of this `Dataset`.

        :type: `string <str>`

        Raises:
            `TecplotSystemError`
        """
        try:
            return _tecutil.DataSetGetInfoByUniqueID(self.uid)[0]
        except AttributeError:
            with self.frame.activated():
                return _tecutil.DataSetGetInfo()[1]

    @title.setter
    @lock()
    def title(self, title):
        try:
            if not _tecutil.DataSetSetTitleByUniqueID(self.uid, title):
                raise TecplotSystemError()
        except AttributeError:
            with self.frame.activated():
                if not _tecutil.DataSetSetTitle(name):
                    raise TecplotSystemError()

    @property
    def num_zones(self):
        """Number of `Zones <Zone>` in this `Dataset`.

        :type: `integer <int>`
        """
        return _tecutil.DataSetGetNumZonesByUniqueID(self.uid)

    def zone(self, pattern):
        """Returns `Zone` by index or string pattern.

        Parameters:
            pattern (`integer <int>` or `string <str>`):  Zero-based index or
                `glob-style pattern <fnmatch.fnmatch>` in which case, the
                first match is returned.

        Raises:
            `TecplotIndexError`

        The `Zone.name` attribute is used to match the *pattern* to the desired
        `Zone` though this is not necessarily unique::

            >>> ds = frame.dataset
            >>> print(ds)
            Dataset:
              Zones: ['Rectangular zone']
              Variables: ['x', 'y', 'z']
            >>> rectzone = ds.zone('Rectangular zone')
            >>> rectzone == ds.zone(0)
            True
        """
        if isinstance(pattern, string_types):
            return next(self.zones(pattern))
        else:
            if pattern < 0:
                pattern += self.num_zones
            if 0 <= pattern < self.num_zones:
                with self.frame.activated():
                    if _tecutil.ZoneIsEnabled(pattern+1):
                        return Zone(_tecutil.ZoneGetUniqueIDByDataSetID(
                                        self.uid, pattern+1), self)
        raise TecplotIndexError

    def zones(self, pattern=None):
        """Yields all `Zones <Zone>` matching a *pattern*."""
        for i in range(self.num_zones):
            try:
                zone = self.zone(i)
                if pattern is None or fnmatch(zone.name, pattern):
                    yield zone
            except TecplotIndexError:
                # zone not enabled
                pass

    @property
    def num_variables(self):
        """Number of `Variables <Variable>` in this `Dataset`.

        :type: `integer <int>`
        """
        return _tecutil.DataSetGetNumVarsByUniqueID(self.uid)

    def variable(self, pattern):
        """Returns the `Variable` by index or string pattern.

        Parameters:
            pattern (`integer <int>` or `string <str>`):  Zero-based index or
                `glob-style pattern <fnmatch.fnmatch>` in which case, the
                first match is returned.

        Raises:
            `TecplotIndexError`

        The `Variable.name` attribute is used to match the *pattern* to the
        desired `Variable` though this is not necessarily unique::

            >>> ds = frame.dataset
            >>> print(ds)
            Dataset:
              Zones: ['Rectangular zone']
              Variables: ['x', 'y', 'z']
            >>> x = ds.variable('x')
            >>> x == ds.variable(0)
            True
        """
        if isinstance(pattern, string_types):
            return next(self.variables(pattern))
        else:
            if pattern < 0:
                pattern += self.num_variables
            if 0 <= pattern < self.num_variables:
                if _tecutil.VarIsEnabledByDataSetID(self.uid, pattern+1):
                    return Variable(_tecutil.VarGetUniqueIDByDataSetID(
                                        self.uid, pattern+1), self)
        raise TecplotIndexError

    def variables(self, pattern=None):
        """Yields all `Variables <Variable>` matching a *pattern*."""
        for i in range(self.num_variables):
            try:
                variable = self.variable(i)
                if pattern is None or fnmatch(variable.name, pattern):
                    yield variable
            except TecplotIndexError:
                # variable not enabled
                pass

    # noinspection PyPep8Naming
    @property
    def VariablesNamedTuple(self):
        """This generates a namedtuple object using variable names.

        .. note::

            The variable names are transformed to be unique, valid
            identifiers suitable for use as the key-list for a
            `collections.namedtuple`. This means that all invalid characters
            such as spaces and dashes are converted to underscores, leading
            numbers and Python keywords are prepended by underscores and
            duplicate variable names are indexed starting with zero.

        Examples:

            This example shows how one can use this n-tuple type with the
            result from a call to `tecplot.data.probe_at_position`::

            >>> from os import path
            >>> import tecplot as tp
            >>> examples_dir = tp.session.tecplot_examples_directory()
            >>> datafile = path.join(examples_dir,'3D_Volume','jetflow.plt')
            >>> dataset = tp.data.load_tecplot(datafile)
            >>> result = tp.data.probe_at_position(0,0.1,0.3)
            >>> data = dataset.VariablesNamedTuple(*result.data)
            >>> msg = '(RHO, E) = ({:.2f}, {:.2f})'
            >>> print(msg.format(data.RHO, data.E))
            (RHO, E) = (1.17, 252930.37)
        """
        names = []
        name_count = {}
        for v in self.variables():
            # sub invalid characters with underscores
            name = re.sub('\W|^(?=\d)', '_', v.name)
            # prepend Python keywords with underscore
            if iskeyword(name):
                name = '_'+name
            if name in name_count:
                name_count[name] += 1
                name = '{}{}'.format(name, name_count[name])
            else:
                name_count[name] = 0
            names.append(name)
        return namedtuple('DatasetVariables', names)

    @lock()
    def copy_zones(self, *zones):
        """Copies `Zones <Zone>` within this `Dataset`."""
        num_zones = self.num_zones
        with IndexSet(*zones) as zoneset:
            with ArgList(SOURCEZONES=zoneset) as arglist:
                log.debug(arglist)
                _tecutil.ZoneCopyX(arglist)
        return [self.zone(i) for i in range(num_zones, self.num_zones)]

    @lock()
    def add_variable(self, name, dtypes=None, locations=None):
        """Add a single `Variable` to the active `Dataset`.

        Parameters:
            name (`string <str>`): The name of the new `Variable`. This does not
                have to be unique.
            dtypes (`FieldDataType` or `list` of `FieldDataType`, optional):
                Data types of this `Variable` for each `Zone` in the currently
                active `Dataset`. Options are: `FieldDataType.Float`, `Double
                <FieldDataType.Double>`, `Int32`, `Int16`, `Byte` and `Bit`. If
                a single value, this will be duplicated for all `Zones <Zone>`.
                (default: `None`)
            locations (`ValueLocation` or `list` of `ValueLocation`, optional):
                Point locations of this `Variable` for each `Zone` in the
                currently active `Dataset`. Options are: `Nodal` and
                `CellCentered`. If a single value, this will be duplicated for
                all `Zones <Zone>`. (default: `None`)

        Raises:
            `TecplotSystemError`
        """
        assert len(name) <= 128, 'Variable names are limited to 128 characters'
        with self.frame.activated():
            dataset = self.frame.dataset
            new_variable_index = dataset.num_variables
            with ArgList(NAME=name) as arglist:
                if dtypes is not None:
                    if not hasattr(dtypes, '__iter__'):
                        dtypes = [dtypes]*dataset.num_zones
                    arglist['VARDATATYPE'] = dtypes
                if locations is not None:
                    if not hasattr(locations, '__iter__'):
                        locations = [locations] * dataset.num_zones
                    arglist['VALUELOCATION'] = locations

                if __debug__:
                    msg = 'new variable: '+name
                    for k, v in arglist.items():
                        msg += '\n  {} = {}'.format(k, v)
                    log.debug(msg)
                if not _tecutil.DataSetAddVarX(arglist):
                    raise TecplotSystemError()
            return dataset.variable(new_variable_index)

    # noinspection PyIncorrectDocstring
    @lock()
    def add_zone(self, zone_type, name, shape, dtypes=None, locations=None,
                 **kwargs):
        """Add a single `Zone` to the active `Dataset`.

        Parameters:
            zone_type (`ZoneType`): The type of `Zone` to be created. Possible
                values are: `Ordered`, `FETriangle`, `FEQuad`, `FETetra`,
                `FEBrick`, `FELineSeg`, `FEPolyhedron` and `FEPolygon`.
            name (`string <str>`): Name of the new `Zone`. This does not have to
                be unique.
            shape (`integer <int>` or `list` of `integers <int>`): Specifies the
                length and dimension (up to three) of the new `Zone`. A 1D
                `Zone` is assumed if a single `int` is given. This is **(i, j,
                k)** for ordered `Zones <Zone>`, **(num_points, num_elements)**
                for finite-element `Zones <Zone>` and **(num_points,
                num_elements, num_faces)** for polytope `Zones <Zone>` where the
                number of faces is known.
            dtypes (`FieldDataType`, `list` of `FieldDataType`, optional): Data
                types of this `Zone` for each `Variable` in the currently
                active `Dataset`. Options are: `FieldDataType.Float`, `Double
                <FieldDataType.Double>`, `Int32`, `Int16`, `Byte` and `Bit`. If
                a single value, this will be duplicated for all `Variables
                <Variable>`. If `None` then the type of the first `Variable`,
                defaulting to `FieldDataType.Float`, is used for all. (default:
                `None`)
            locations (`ValueLocation`, `list` of `ValueLocation`, optional):
                Point locations of this `Zone` for each `Variable` in the
                currently active `Dataset`. Options are: `Nodal` and
                `CellCentered`. If a single value, this will be duplicated for
                all `Variables <Variable>`.  If `None` then the type of the
                first `Variable`, defaulting to `Nodal`, is used for all.
                (default: `None`)
            parent_zone (`Zone`, optional): A parent `Zone` to be used when
                generating surface-restricted streamtraces.
            solution_time (`float`, optional): (default: 0)
            strand_id (`integer <int>`, optional): Associate this new `Zone`
                with a particular strand.

        Raises:
            `TecplotSystemError`
        """
        if __debug__:
            if self.num_variables == 0:
                errmsg = dedent('''\
                Can not create a zone on a dataset with no variables.
                    Add at least one variable to this dataset before
                    creating any zones.''')
                raise TecplotLogicError(errmsg)
        kwargs = {k.replace('_', '').upper(): v for k, v in kwargs.items()}
        with self.frame.activated():
            dataset = self.frame.dataset
            new_zone_index = dataset.num_zones
            with ArgList(ZONETYPE=zone_type, NAME=name) as arglist:
                # convert shape to (imax, jmax, kmax)
                if not hasattr(shape, '__iter__'):
                    shape = [shape]
                for k, v in zip([sv.IMAX, sv.JMAX, sv.KMAX], shape):
                    arglist[k] = v

                # expand data types and locations to length of num_variables
                for key, val in zip([sv.VARDATATYPE, sv.VALUELOCATION],
                                    [dtypes, locations]):
                    if val is not None:
                        if not hasattr(val, '__iter__'):
                            val = [val]*dataset.num_variables
                        arglist[key] = val

                # ensure floating-point params are floats
                float_args = [sv.SOLUTIONTIME]
                for a in float_args:
                    if a in kwargs:
                        kwargs[a] = float(kwargs[a])

                # convert objects to indexes
                index_args = [sv.ZONE, sv.CONNECTSHAREZONE]
                for a in index_args:
                    if a in kwargs:
                        kwargs[a] = kwargs[a].index + 1

                arglist.update(**kwargs)

                if __debug__:
                    shp = '({})'.format(','.join(str(s) for s in shape))
                    msg = 'new dataset shape: '+shp
                    for k, v in arglist.items():
                        msg += '\n  {} = {}'.format(k, v)
                    log.debug(msg)

                if not _tecutil.DataSetAddZoneX(arglist):
                    raise TecplotSystemError()

            return dataset.zone(new_zone_index)

    def add_ordered_zone(self, name, shape, dtypes=None, locs=None, **kwargs):
        return self.add_zone(ZoneType.Ordered, name, shape, dtypes, locs,
                             **kwargs)

    def add_fe_zone(self, zone_type, name, num_points, num_elements,
                    dtypes=None, locs=None, **kwargs):
        assert zone_type in [ZoneType.FETriangle, ZoneType.FEQuad,
                             ZoneType.FETetra, ZoneType.FEBrick,
                             ZoneType.FELineSeg]
        return self.add_zone(zone_type, name, (num_points, num_elements),
                             dtypes, locs, **kwargs)

    def add_poly_zone(self, name, zone_type, num_points, num_elements,
                      num_faces, **kwargs):
        assert zone_type in [ZoneType.FEPolyhedron, ZoneType.FEPolygon]
        return self.add_zone(zone_type, name, (num_points, num_elements,
                             num_faces), dtypes, locs, **kwargs)

    @lock()
    def delete_variables(self, *variables):
        """Remove `Variables <Variable>` from this `Dataset`.

        Parameters:
            *variables (`Variable` or index `integer <int>`): Variables to
                remove from this dataset.

        .. code-block:: python
            :emphasize-lines: 3

            >>> print([v.name for v in dataset.variables()])
            ['X','Y','Z']
            >>> dataset.delete_variables(dataset.variable('Z'))
            >>> print([v.name for v in dataset.variables()])
            ['X','Y']

        Notes:
            Multiple `Variables <Variable>` can be deleted at once, though
            the last `Variable` can not be deleted. This command deletes all
            but the first `Variable` in the `Dataset` (usually ``X``)::

                dataset.delete_variables(dataset.variables())
        """
        variables = flatten_args(*variables)
        with self.frame.activated():
            with IndexSet(*variables) as vlist:
                _tecutil.DataSetDeleteVar(vlist)

    @lock()
    def delete_zones(self, *zones):
        """Remove `Zones <Zone>` from this `Dataset`.

        Parameters:
            *zones (`Zone` or index `integer <int>`): Zones to remove from
                this dataset.

        .. code-block:: python
            :emphasize-lines: 3

            >>> print([z.name for z in dataset.zones()])
            ['Zone 1', 'Zone 2']
            >>> dataset.delete_zones(dataset.zone('Zone 2'))
            >>> print([z.name for z in dataset.zones()])
            ['Zone 1']

        Notes:
            Multiple `Zones <Zone>` can be deleted at once, though the last
            `Zone` can not be deleted. This command deletes all but the
            first `Zone` in the `Dataset`::

                dataset.delete_zones(dataset.zones())
        """
        zones = flatten_args(*zones)
        with self.frame.activated():
            with IndexSet(*zones) as zlist:
                _tecutil.DataSetDeleteZone(zlist)


@property
@lock()
def dataset(frame):
    """`Dataset` attached to this `Frame`.

    Returns:
        `Dataset`: The object holding onto the data associated with this
        `Frame`.

    If no `Dataset` has been created for this `Frame`, a new one is created
    and returned.
    """
    with frame.activated():
        if not _tecutil.DataSetIsAvailableForFrame(frame.uid):
            frame.create_dataset(frame.name+' Dataset')
        return Dataset(_tecutil.DataSetGetUniqueID(), frame)


@property
def has_dataset(frame):
    """Checks to see if the `Frame` as an attached `Dataset`

    Returns:
        `bool`: `True` if the `Frame` has a `Dataset`
    """
    with frame.activated():
        return _tecutil.DataSetIsAvailableForFrame(frame.uid)

layout.Frame.dataset = dataset
layout.Frame.has_dataset = has_dataset
