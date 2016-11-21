"""
Common types for collection (like Capacity, etc...)
"""


#######################################################################################################################
# Base classes
#######################################################################################################################

class Bases(object):
    BASE_10 = 10.0
    BASE_1000 = 1000.0
    BASE_1024 = 1024.0


class Units(object):
    BYTES = "Bytes"
    KB = "KB"
    MB = "MB"
    GB = "GB"
    TB = "TB"

    BYTES_PER_SEC = "Bytes/s"
    KB_PER_SEC = "KB/s"
    MB_PER_SEC = "MB/s"
    GB_PER_SEC = "GB/s"
    TB_PER_SEC = "TB/s"

    IO = "IO"
    IO_PER_SEC = "IO/s"
    QUERY_PER_SEC = "Query/s"

    US = "us"
    MS = "ms"
    SEC = "sec"

    HZ = "Hz"
    KHZ = "KHz",
    MHZ = "MHz",
    GHZ = "GHz",

    HOURLY = "hourly"
    DAILY = "daily"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class DataType(object):
    """
    Base class for defining a data type.

    A data type is an arbitrary structure with meta-data describing this value. This type will be registered in the
    dictionary for later display and aggregation purposes.
    """
    def __init__(self, **kwargs):
        """
        :param str label: Short label
        :param str description: Full description (documentation) for this type
        :param bool visible: If True, this type will be visible by default
        :param bool importance: indicator (can be used by the UI) 0 most important
        """
        self._label = kwargs.get("label")
        self._importance = kwargs.get("importance", 1000)
        self._description = kwargs.get("description")
        self._visible = kwargs.get("visible", True)

    @classmethod
    def get_type(cls):
        name = cls.__name__
        assert name.endswith("DataType"), "Wrong name format: {}".format(name)
        return name[:-8]

    @property
    def type(self):
        return self.__class__.get_type()

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    @property
    def importance(self):
        return self._importance

    @importance.setter
    def importance(self, value):
        self._importance = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value

    @property
    def meta_data(self):
        """
        Given a meta data dict for this field, include additional information available about this type

        :rtype: dict
        """

        # Use the attribute names as keys in the meta-data dict as well as properties to look up 'self'
        props = ("type", "label", "description", "importance", "visible",)
        return {p: getattr(self, p) for p in props if getattr(self, p, None) is not None}

    def __repr__(self):
        return "{} (label={})".format(self.type, self.label)

    def __eq__(self, other):
        return type(self) == type(other)


class DataTypeWithUnit(DataType):
    """
    A data type with unit. This class adds the concepts of unit conversions, including support for different bases
    (e.g. 1000, 1024).

    All deriving class MUST define the following two class based attributes:

    1. Units_def: Defines which units are available for this type
    The first element in the tuple is a dict of unit to unit_exp. The second defines the most basic unit
    exponent for this type (e.g. 0: Bytes for capacity)

    2. Bases_def: A set of all possible bases for the unit calculation.
    """
    units_def = None
    bases_def = None
    default_unit = None
    default_base = None

    UNIT = "unit"
    BASE = "base"

    def __init__(self, **kwargs):
        super(DataTypeWithUnit, self).__init__(**kwargs)

        assert self.__class__.units_def, "Child Class must override units_def"
        assert self.__class__.bases_def, "Child Class must override bases_def"

        # Validate unit and base...
        # The class must have two attributes (two tuples): units_def and bases_def. Both define how to calculate and
        # convert values of this type
        units = self.__class__.units_def
        bases = self.__class__.bases_def

        unit = kwargs.get("unit") or self.default_unit or self.__class__.units_def[0]
        assert unit is not None and unit in units, \
            "{} - Invalid unit {}, can only be one of {}".format(self.type, unit, units)

        base = kwargs.get("base") or self.default_base or self.__class__.bases_def[0]
        assert base and base in bases, "{} - Invalid base {}, can only be one of {}".format(self.type, base, bases)

        # Save the unit and base as they were given - so we can do conversions later
        self._unit = unit
        self._base = base

    @property
    def units(self):
        """
        :rtype: tuple[str]
        """
        return self.__class__.units_def

    @property
    def bases(self):
        """
        :rtype: tuple[str]
        """
        return self.__class__.bases_def

    @property
    def unit(self):
        return self._unit

    @property
    def base(self):
        return self._base

    def __repr__(self):
        return "{}(label={}, unit={}, base={})".format(self.type, self.label, self.unit, self.base)

    def convert(self, value, from_unit=None, from_base=None, to_unit=None, to_base=None):
        """
        Return the value of this type converted to the required unit (and optional base)

        :param float value: Value to convert
        :param str|None from_unit: Unit to convert from (if none, self.unit will be used)
        :param float|None from_base: Base to convert from (optional - if missing, the self.base will be used)
        :param str to_unit: Unit to convert to (if none, self.unit will be used)
        :param float|None to_base: Base to convert to (optional - if missing, self.base will be used)

        :return: the converted value
        :rtype: float
        """

        assert from_unit or from_base or to_unit or to_base, "Some conversion action is expected..."

        # The class must have two attributes (two tuples): units_def and bases_def. Both define how to calculate and
        # convert values of this type

        units = self.__class__.units_def
        bases = self.__class__.bases_def

        from_unit = from_unit or self.unit
        assert from_unit in units, "Invalid from_unit {}, can only be one of {}".format(from_unit, units)

        to_unit = to_unit or self.unit
        assert to_unit in units, "Invalid to_unit {}, can only be one of {}".format(to_unit, units)

        from_base = from_base or self.base
        assert from_base in bases, "Invalid from_base {}, can only be one of {}".format(from_base, bases)

        to_base = to_base or self.base
        assert to_base in bases, "Invalid to_base {}, can only be one of {}".format(to_base, bases)

        ratio = from_base / to_base
        value *= ratio

        exp_diff = units.index(from_unit) - units.index(to_unit)
        value *= to_base ** exp_diff

        return value

    @property
    def meta_data(self):
        meta = super(DataTypeWithUnit, self).meta_data

        meta.update({
            "units": list(self.units),  # Used by GUI - to allow a selection box
            "bases": list(self.bases),  # Used by GUI - to allow a selection box
            "unit": self.unit,
            "base": self.base,
        })

        return meta


class TypedValue(object):
    """
    Value associated with a data type.
    """

    def __init__(self, value, data_type):
        """
        :type data_type: DataType
        """
        assert isinstance(data_type, DataType), "Expecting data_type to be a subclass of DataType"

        self._value = value
        self._data_type = data_type

    @property
    def value(self):
        return self._value

    @property
    def data_type(self):
        return self._data_type

    @property
    def meta_data(self):
        return self._data_type.meta_data

    def __eq__(self, other):
        if not isinstance(other, TypedValue) or self.data_type != other.data_type:
            return False
        return self.value == other.value

    def __gt__(self, other):
        assert isinstance(other, TypedValue) and self.data_type == other.data_type, "Bad types {} <> {}".format(
            self.data_type,
            other.data_type)

        return self.value > other.value

    def __ge__(self, other):
        assert isinstance(other, TypedValue) and self.data_type == other.data_type, "Bad types {} <> {}".format(
            self.data_type,
            other.data_type)

        return self.value >= other.value

    def __lt__(self, other):
        assert isinstance(other, TypedValue) and self.data_type == other.data_type, "Bad types {} <> {}".format(
            self.data_type,
            other.data_type)

        return self.value < other.value

    def __le__(self, other):
        assert isinstance(other, TypedValue) and self.data_type == other.data_type, "Bad types {} <> {}".format(
            self.data_type,
            other.data_type)

        return self.value <= other.value

    def __str__(self):
        return "{}={}".format(self.data_type, self.value)


class RealTypedValue(TypedValue):
    def __init__(self, value, data_type):
        """
        :type value: float
        :type data_type: DataType
        """
        super(RealTypedValue, self).__init__(float(value), data_type)
        assert isinstance(data_type, DataType), "{} is not a subclass of DataType".format(data_type)

    def __add__(self, other):
        if isinstance(other, TypedValue):
            assert self.data_type == other.data_type
            value_to_sub = other.value
        else:
            value_to_sub = float(other)

        return RealTypedValue(self.value + value_to_sub, self.data_type)

    def __sub__(self, other):
        if isinstance(other, TypedValue):
            assert self.data_type == other.data_type
            value_to_sub = other.value
        else:
            value_to_sub = float(other)

        return TypedValue(self.value - value_to_sub, self.data_type)

    def __mul__(self, other):
        if isinstance(other, TypedValue):
            assert self.data_type == other.data_type
            value_to_mul = other.value
        else:
            value_to_mul = float(other)

        return TypedValue(self.value * value_to_mul, self.data_type)

    def __div__(self, other):
        if isinstance(other, TypedValue):
            assert self.data_type == other.data_type
            value_to_div = other.value
        else:
            value_to_div = float(other)

        return TypedValue(self.value / value_to_div, self.data_type)


class RealTypedValueWithUnit(RealTypedValue):
    """
    A value with a data type and a unit.
    """

    def __init__(self, data_type, value, unit=None, base=None):
        """
        :type value: float|tuple[float]
        :param unit: Unit for this value. If None, the DataType's normal unit is used
        :type unit: str
        :param base: Bast for this value. If None, the DataType's normal base is used
        :type base: float
        :type data_type: DataTypeWithUnit
        """
        super(RealTypedValueWithUnit, self).__init__(value, data_type)

        assert isinstance(data_type, DataTypeWithUnit), "Expecting data_type to be a subclass of DataTypeWithUnit"
        assert unit is None or unit in data_type.units, "unit {} must one of {}".format(unit, data_type.units)
        assert base is None or base in data_type.bases, "base {} must one of {}".format(base, data_type.bases)

        if unit and (unit != data_type.unit or base != data_type.base):
            self._value = data_type.convert(self._value, from_unit=unit, from_base=base)

    @property
    def data_type(self):
        """
        :rtype: DataTypeWithUnit
        """
        return super(RealTypedValueWithUnit, self).data_type

    # noinspection PyUnresolvedReferences
    def convert(self, to_unit, to_base=None):
        """
        Shortcut method to convert the value to another unit

        :rtype: float
        """
        return self.data_type.convert(value=self.value, to_unit=to_unit, to_base=to_base)


#######################################################################################################################
# Primitive / Basic data types
#
# These types define primitives (in terms of units) supported by the system
#######################################################################################################################

class CapacityDataType(DataTypeWithUnit):
    units_def = (Units.BYTES, Units.KB, Units.MB, Units.GB, Units.TB,)
    bases_def = (Bases.BASE_1000, Bases.BASE_1024,)
    default_unit = Units.GB
    default_base = Bases.BASE_1024


def capacity_value(value, unit=None, base=None, label=None, description=None, visible=True, importance=120):
    data_type = CapacityDataType(label=label, description=description, visible=visible, importance=importance)
    return RealTypedValueWithUnit(data_type=data_type, value=value, unit=unit, base=base)


class ThroughputDataType(DataTypeWithUnit):
    units_def = (Units.BYTES_PER_SEC, Units.KB_PER_SEC, Units.MB_PER_SEC, Units.GB_PER_SEC, Units.TB_PER_SEC,)
    bases_def = (Bases.BASE_1000, Bases.BASE_1024,)
    default_unit = Units.MB_PER_SEC
    default_base = Bases.BASE_1024


def throughput_value(value, unit=None, label=None, description=None, visible=True, importance=13):
    data_type = ThroughputDataType(label=label, description=description, visible=visible, importance=importance)
    return RealTypedValueWithUnit(data_type=data_type, value=value, unit=unit)


class PercentDataType(DataTypeWithUnit):
    units_def = ("%",)
    bases_def = (Bases.BASE_10,)


def percent_value(value, unit=None, label=None, description=None, visible=True, importance=13):
    data_type = PercentDataType(label=label, description=description, visible=visible, importance=importance)
    # Internally, values are kept as ratios (between 0.0 and 1.0)
    return RealTypedValueWithUnit(data_type=data_type, value=value / 100.0, unit=unit)


class FrequencyDataType(DataTypeWithUnit):
    units_def = (Units.HZ, Units.KHZ, Units.MHZ, Units.GHZ,)
    bases_def = (Bases.BASE_1000,)
    default_unit = Units.MHZ


class IOsDataType(DataTypeWithUnit):
    units_def = (Units.IO,)
    bases_def = (Bases.BASE_10,)


def ios_value(value, label=None, description=None, visible=True, importance=15):
    data_type = IOsDataType(label=label, description=description, visible=visible, importance=importance)
    return RealTypedValueWithUnit(data_type=data_type, value=value)


class IOpsDataType(DataTypeWithUnit):
    units_def = (Units.IO_PER_SEC,)
    bases_def = (Bases.BASE_10,)


def iops_value(value, label=None, description=None, visible=True, importance=12):
    data_type = IOpsDataType(label=label, description=description, visible=visible, importance=importance)
    return RealTypedValueWithUnit(data_type=data_type, value=value)


class CountDataType(DataTypeWithUnit):
    units_def = ("",)
    bases_def = (Bases.BASE_10,)


def count_value(value, label=None, description=None, visible=True, importance=17):
    data_type = CountDataType(label=label, description=description, visible=visible, importance=importance)
    return RealTypedValueWithUnit(data_type=data_type, value=value)


class RateDataType(DataTypeWithUnit):
    units_def = ("unit/s",)  # Typically these are over written by implementing classes (with more specific units)
    bases_def = (Bases.BASE_10,)


class PricePerPeriodDataType(DataTypeWithUnit):
    units_def = (Units.HOURLY, Units.DAILY, Units.MONTHLY, Units.YEARLY)
    bases_def = (Bases.BASE_10,)  # there are in average 730 hours in 1 month
    default_unit = Units.MONTHLY

    def convert(self, value, from_unit=None, from_base=None, to_unit=None, to_base=None):
        """
        Implement convert differently since time is not in decimal base
        """
        assert to_base == Bases.BASE_10, "Cannot change base for price"

        units = self.__class__.units_def

        from_unit = from_unit or self.unit
        assert from_unit in units, "Invalid from_unit {}, can only be one of {}".format(from_unit, units)

        to_unit = to_unit or self.default_unit
        assert to_unit in units, "Invalid from_unit {}, can only be one of {}".format(from_unit, units)

        if from_unit == to_unit:
            return value

        # Convert to hours
        if from_unit == Units.DAILY:
            # there 24 hours in 1 day
            hour_value = value / 24.0
        elif from_unit == Units.MONTHLY:
            # there 730 hours in 1 month in average
            hour_value = value / 730.0
        elif from_unit == Units.YEARLY:
            # there 8760 hours in a year
            hour_value = value / 8760.0
        else:
            assert from_unit == Units.HOURLY, "Unsupported unit '{}'".format(from_unit)
            hour_value = value

        if to_unit == Units.DAILY:
            # there 730 hours in 1 month in average
            new_value = hour_value * 24.0
        elif to_unit == Units.MONTHLY:
            new_value = hour_value * 730.0
        elif to_unit == Units.YEARLY:
            # there 730 hours in 1 month in average
            new_value = hour_value * 8760.0
        else:
            assert to_unit == Units.HOURLY, "Unsupported unit '{}'".format(from_unit)
            new_value = hour_value

        return new_value


def price_value(value, unit=None, label=None, description=None, visible=True, importance=12):
    data_type = PricePerPeriodDataType(label=label,
                                       unit=unit,
                                       description=description,
                                       visible=visible,
                                       importance=importance)
    return RealTypedValueWithUnit(data_type=data_type, value=value)


class TimePeriodDataType(DataTypeWithUnit):
    units_def = (Units.US, Units.MS, Units.SEC,)
    bases_def = (Bases.BASE_1000,)
    default_unit = Units.MS


class UnixDateDataType(DataTypeWithUnit):
    """
    Represents a data (Unix timestamp - secs since epoch)
    """
    units_def = (Units.SEC,)
    bases_def = (Bases.BASE_10,)  # there are in average 730 hours in 1 month
    default_unit = Units.SEC


def unix_date_value(value, label=None, description=None, visible=True, importance=120):
    data_type = UnixDateDataType(label=label, description=description, visible=visible, importance=importance)
    return RealTypedValueWithUnit(data_type=data_type, value=value)


