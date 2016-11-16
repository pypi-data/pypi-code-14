"""
The "user interface" for Dunshire.

Clients are intended to import everything from this module, which in
turn pulls in everything that they would need to use the library.
"""

# Needed to construct the cone over which the game takes place.
from .cones import (NonnegativeOrthant,
                    IceCream,
                    SymmetricPSD,
                    CartesianProduct)

from .games import SymmetricLinearGame
