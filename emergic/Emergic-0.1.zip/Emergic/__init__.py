##################################################################################################################################
# Emergic.py - I manage emergic networks - dynamic, temporal & highly recurrent systems made up of computational unit 
#
# (C) 2008-2009 David Pierre Leibovitz
#
# This system is based on Cognitive Emergantism.
# The heart is based on the concept of temporal and spatial change.
# 1) Recurring change needs to be detected (via correlations and such)
# 2) Future change can be predicted
# 3) Things that don't change can be ignored.
# 4) Links do not have weights (although computations can do so on ports)
# Everything must be biologicaly plausible, including local only computions - no backprop!
#
# Note: This Python code is very C++ish to allow for direct translation.
# Note: This code is meant to be easily converted to integrated circuits (ICs), barring debugging stuff.
#
# Time:
#       1)  Time is measured in ticks.
#           a)  The tick period is constant.
#               Many algorithms don't care about absolute time, but only relative time
#           b)  Of course, the tick period could be thought of as the smallest amount that can be
#               utilized in a cognitive manner. This could be 1ms for the more sensitive "neorons".
#       2)  There are only two types of timings that matter, and only two types of scheduling systems
#           a)  Values are passed between "neurons" via links. These links have a minimal delay of one tick.
#               However, the value/link delay can be specified in three places
#               1)  The link's time delay (TD) which is >= 1. This is meant to be static (except under development)
#               2)  The port's output time delay (oTD) which is usually 0 but can by dynamic.
#               3)  The unit's output time delay (oTD) which is usually 0 but can be dynamic
#           b)  Values can trigger a unit for computation. However, the first value received can trigger the computation into the future,
#               so that multiple values at varying times can be temporally integrated. This computation/unit delay can be specified in two places
#               1)  The unit's input time delay (iTD) which is usually 0 but can be dynamic
#               2)  The port's input time delay (iTD) which is usually 0 but can be dynamic
#       3)  Although a unit's iTD is usually zero, the link's minimal delay of 1 tick ensures that
#           all computations from one unit to the next are seperated by a minimal amount of time.
#
# Major classes
#
#   ChangeUnit - a computational unit (similar to a group of neurons) that
#                   - gets (reads)  information from input ports, and
#                   - sets (writes) information to   output ports
#                Different types of units perform different types of computations.
#                Typically, a unit has one (or limited numbers of) output ports,
#                and one or more input ports.
#                - Units do not have a computational time delay (td) because
#                  this can be factored into the time delay of each output link.
#                  (Although in the future we could have a dynamic quantity - link delays are static)
#
#Each unit has a minimal computational time delay (td) of one tick.
#                  (Likely not needed because of link delays)
#                - Each unit has a minimal time constant (tc) of one (Zero?) tick, i.e.,
#                  When its first input is triggered
#
#   ChangePort - A port is a unit's interface to other units (via links).
#                Analogized as a set of synapses.
#                Sensors/effectors (transducers) can be simply ports connected to the environment.???
#
#   ChangeLink - A link connects (one way) a unit's output port to another unit's input port.
#                Analogized as a set of nerve fibers (outgoing axons or incomming dendrites).
#
#                An output port can be one-to-many - the port value will be sent along each link.
#                An input port can only be a singlet.??? or allow arrays???
#                - Each link has a minimal transmission time delay (td) of one tick.
#                  This is meant to be static (except perhaps during phisical development?)
#
#   ChangeValue- Typically the value plus an error? Time?
#                These are queued??? Multiple values can be in a link connecting a fast outputer to a slow inputter?
#                Just allow current and last value for now???
#
# Timing:
#    The system is currently temporally ordered only. However, for more realisting absolute times purpses,
#    - Default link delays should be 10 (to allow for faster links).
#    - Defaut computation delays should be ???.
#
# Ports and links do not have weights. Learning can only consist of
# 1) changing port values
# 2) creating or destroying links
# 3) creating or destroying units (ports are not creatable or destructible???)
# 4) Changing internal computional values (should all these be placed in unused ports?)
#
# Diagramming conventions.
# Units have specific shapes for specific purposes.
# Where they are purely spatial, they reflect 2-D geometry.
# Where they are temporal...
# t-3 t-2 t-1 t t+1 t+2 t+3
# High Level
# Low  Level
#
#    /\
#  <Unit>
#    \/
# Processing Order:
# =================
#
# Network is meant to be asynchronous.
# For simplification, each unit is a proper function of its inputs (and internal states).
#    There is no decay. There is no random number generators - this can be put in the environment.
# When a port is set, each following unit is queued for execution based on the link delay, plus it's time constant.
# 1) A unit does not become queued unless an input port CHANGES its value. This will reduce infinite loops.
#    In general, loops are not discouraged. #queued times will be counted in order to detect poorly designed networks.
#
# Naming Convention:
# ==================
# There are globally unique network names and network IDs as well as local variants.
# The names are retained across cloning, while the IDs increment.
# Moreover, there is a single uppercase prefix for each type of entity
# +--------+------+-------+-------+
# |Element |Prefix|Global |Local  |
# |        |      +----+--+----+--+
# |        |      |Name|ID|Name|ID|
# +--------+------+----+--+----+--+
# |Network |   N  |  1 |1 |mind|1 |
# |Group   |   G  |1,2,3|
# |Unit    |   U  |
# |Port    |   P  |
# |Link    |   L  |

"""
Implement the change network.

Author: David Pierre Leibovitz (C) 2008-2009
"""

dbgTraceSched = False        # Determine whether scheduling should be traced.

from entity  import Entity
from network import Network
from unit    import Unit
from port    import Port, PortFirst, PortUnique, PortSum, PortMaxAmount, PortMaxConfidence
from link    import Link
from value   import Value    

