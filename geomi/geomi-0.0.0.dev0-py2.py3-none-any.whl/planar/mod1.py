"""
This is a module containing functions on planar geometry.

:Description:
    Functions in this module enable simple calculations:
    + Find the distance between two points
    + Find the intersecting points of two lines/curves
    + Find the axis intercepts of lines/curves
    + Find the local min/max of curves
    + Find the area between two lines/curves
    + Find the area within closed shapes (triangles, polygons)
    + Find the angle between two intersecting lines

    For some functions there is support for both Cartesian as well
    as Polar coordinate systems. Please consult the documentation
    at function level.

:Dependencies:
    + numpy: basic requirement for all math computations
    
:Todo:
    + Find the perpendicular distance from a point to a line
    + Transformations such as rotating a line by x radians
    + Asymptotes of a hyperbola
"""

# Implicit absolute
import geomi
import geomi.solid
import geomi.planar.mod2

# Explicit absolute
from geomi import solid
from geomi.utils import algos
from geomi.planar.mod2 import func1

# Explicit relative
from . import mod2
from .mod2 import func1
from ..solid import mod1

# Implicit absolute (not allowed)
#import .mod2
#import .mod2.func
#import ..solid.mod1


class Planar1():
    """Docstring for class Foo."""

    #: Doc comment for class attribute Foo.bar.
    #: It can have multiple lines.
    bar = 1

    flox = 1.5   #: Doc comment for Foo.flox. One line only.

    baz = 2
    """Docstring for class attribute Foo.baz comes after the attribute."""

    def __init__(self):
        self.qux = 3 #: Comment on a single line for an instance attribute.

        self.spam = 4
        """Docstring for instance attribute spam comes after the attribute.
        This could be very descriptive and spanning multiple lines."""

    def func_in(self):
        """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        
        Cras viverra mollis pharetra. Nam semper, lectus sit amet tincidunt maximus, nibh tellus accumsan neque, ac varius lacus ante nec augue. Maecenas volutpat sed ipsum ut lacinia. Ut sed consectetur libero. Mauris velit est, scelerisque quis libero eget, aliquet blandit est. Donec bibendum odio et velit convallis, et scelerisque ante fermentum. Duis congue sem ex, at semper turpis egestas nec. Aenean eu condimentum orci, ac efficitur nulla. Etiam facilisis varius quam, at ultrices lectus semper eget. Suspendisse ultrices eros eu porttitor ornare. Nunc vitae diam ultricies, interdum mi a, faucibus leo.
        """
        pass


def func1(name, state=None):
    """This function does something.

    :param name: The name to use. 
    :type name: str
    :param state: Current state to be in. 
    :type state: bool
    :returns: int: error code that is non-zero if in error.
    :raises: AttributeError, KeyError
    """ 
    return 0

