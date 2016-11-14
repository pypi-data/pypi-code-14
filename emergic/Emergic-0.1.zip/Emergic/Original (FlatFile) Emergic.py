##################################################################################################################################
# Emergic.py - I manage emergic networks - dynamic, temporal & highly recurrent systems made up of computational unit 
#
# (C) 2008 David Pierre Leibovitz
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

Author: David Pierre Leibovitz (C) 2008
"""

import copy                 # copy.copy() - shallow copy

dbgTraceSched = False        # Determine whether scheduling should be traced.
    
##################################################################################################################################
class Entity(object):
    """I am the supermost ancestral derivational object for all entities in the emergic module.

    I am used for common debugging purposes only.
    """

    dbgInstances = []   # A quick debugging access to all Entities. See dbgDumpLinks().
    
    #-----------------------------------------------------------------------------------------------------------------------------
    def __init__(self, name):                                                                               # of Emergic.Entity
        """Create the common nameing, debugging, and analytical object for all entities in the emergic system.

        namePrefix  - a single uppercase letter used as a prefix for all my names
          =N:       I am a network
          =G:       I am a group
          =U:       I am a unit
          =P:       I am a port (use I=Input and O=Output instead?)
          =L:       I am a link

        network     My global network
          =None:    only when I am the global network entity itself
  
        nameGlobal  My globally unique name, retained after cloning
        idGlobal    My globally unique number, incremented with cloning.

        nameLocal   My locally unique name,   retained after cloning
        idLocal     My locally unique number, increment with each clone

        ancestor    My ancestor
        descendants My descendants
        """
        self.dbgName    = name      # My debug name
        self.dbg        = False     # Debug me specifically, rather than all generically
        #self.nameGlobal  = None
        #self.nameLocal   = dbgGlobal
        Entity.dbgInstances.append(self)

    #-----------------------------------------------------------------------------------------------------------------------------
    def error(self, text):                                                                                  # of Emergic.Entity
        """Print an error message with respect to this entity."""
        print("Error (" + self.dbgName + "): " + text)

##################################################################################################################################
class Network(Entity):
    """I am a network of computational units managing change in some fashion.

    Units receive information from their input ports, and transmit information to their output ports.

    Links serve to connect the ports of one unit to others to form the network. Diagramatically:

    +---------+            +----------------+
    |Unit#1   |            |Unit#2          |                              1) Links are highly recurrent leading to emergic behaviour
    |  +------+            +------+  +------+
    |  |Output|---Link#1-->|Input |  |Output|---Link#6-->To other units    2) Ports can distribute values to multiple units
    |  |Port#1|            |Port#3|  |Port#5|---Link#7-->
    |  +------+            +------+  +------+
    |         |            |                |
    |  +------+            +------+  +------+
    |  |Input |<--Link#2---|Output|  |Input |<--Link#8---From other units  3) Ports can receive values from multiple units
    |  |Port#2|            |Port#4|  |Port#6|<--Link#9---                     BUT only one (undetermined) value ever accessed
    |  +------+            +------+  +------+
    |         |            |                |
    +---------+            +----------------+
    """

    dbgInstances        = 0     # Count of network instances. Only one is allowed for now.
    
    # Not currently used, but if realistic timings which allow desensitizing and ...
    realisticUnitITD    = 5     # ??? Realistic default value
    realisticUnitOTD    = 3     # ???
    realisticLinkTD     = 3     # ???

    #-----------------------------------------------------------------------------------------------------------------------------
    def __init__(self, name=None):                                                                          # of Emergic.Network
        """Create an emergic network that manages a set of computational units interconnected by links.

        I should be the only network in existence! ???Not tested for???

        name        My name for debugging purposes (just to be consistent with all other classes) (defualt=N1)
           =None:   Assign the next available global network number, e.g., N1, N2, N3, ...
                    Of course, this system only supoorts 1 network!
           else:    Use name as specifed. By convention, network names start with an uppercase 'N'.
        """

        Network.dbgInstances += 1
        if not name: name = "N" + str(Network.dbgInstances)
        Entity.__init__(self, name)

        self.time           = 0     # Current time in ticks.
                                    # The value of 0 can never occur, as a link minimally delays the first execution to 1.
                                    # Therfore, 0 is used to indicate that a unit is not queued for execution.
                                    # This system is meant to be temporaly ordered but durations need not be realistic.
                                    # Assume each tick is 1/10th of a millisecond???
                                    # (Should have better relative time delays).

        self.dbgUnits       = []    # List of units in the network for debugging purposes. Length used as unit count.
        self.dbgPorts       = 0     # Number of ports in the network for debugging purposes.
        self.dbgSrcLinks    = 0     # Number of source      links in the network for debugging purposes.
        self.dbgDstLinks    = 0     # Number of destination links in the network for debugging purposes.
                                    # Src and dst link counts need not be identical if
                                    # a) links can cross networks (currently not supported)
                                    # b) links can develope from src to dst in time (or v.s., currently not supported)
        #self.dbgGroups      = []    # List of groups in the network for debugging purposes. Length used as group count.
    
        self.qValues        = {}    # List of values queued for delivery to destination unit ports.
                                    # Arranged in a dictionary, where the
                                    #    key: the dequeue time (having factored in the originating unit's OTD and the link's TD)
                                    #    entry: list of (value,link) tupples
                                    #        value: the value being delivered from a source to destination port
                                    #        link:  the link over which this value is delivered
                                    # Looks like qTime:[(value,link)]
                                    # Values are dequeued before units.
                                    # When a value is dequeued, it is possible that a unit becomes queued for the same time based on it's ITD=0.
                                    # However, when a unit becomes dequeued, values canot be queued at the same time as a link's TD>=1.
                                    # Thus, there are no infinite loops in the dequeuing/scheduling system.
                                    # When all values for the current time have been dequeued, the entire dictionary entry is deleted.

        self.qUnits         = {}    # A list of units queued for execution.
                                    # Arranged in a dictionary, where the
                                    #    key:   is the dequeue time,
                                    #    entry: list of units
                                    # Looks like qTime:[unit]
                                    # Units are dequeued after values.
                                    # When all units for the current time have been dequeued, the entire dictionart entry is deleted.

        # These debug counters measure unit, port and link utilization (activity) per tick and entire run.
        # 1) ??? They could be averaged and windowed to measure neuronal activity "a la" MRIs.
        # 2) ??? Activity can be used for development purposes as well.
        # These counters are repeated within units, ports and links as required.
        #
        # These counters are for the current tick (they don't have "tick" in their names as they are used throughout)
        self.dbgPortTxIgnored       = 0 # Number of values not queued for transmission through ports
        self.dbgPortTxHandled       = 0 # Number of values   enqueued for transmission through ports
        self.dbgPortRxIgnored       = 0 # Number of port values not consumed by unit computations
        self.dbgPortRxHandled       = 0 # Number of port values     consumed by unit computations
        self.dbgLinkTxIgnored       = 0 # Global number of values not queued fir transmission through links (many links per port)
        self.dbgLinkTxHandled       = 0 # Global number of values   enqueued for transmission through links (many links per port)
        self.dbgLinkRxIgnored       = 0 # Global number of value dequeues ignored by links & ports
        self.dbgLinkRxHandled       = 0 # Global number of value dequeues handled by links & ports
        self.dbgUnitComputes        = 0 # Global number of unit computations

        # These counters are for the entire run; Ports, links & units have entire run counters as well.
        self.dbgRunPortTxIgnored = 0; self.dbgRunPortTxHandled = 0; self.dbgRunPortRxIgnored = 0; self.dbgRunPortRxHandled = 0
        self.dbgRunLinkTxIgnored = 0; self.dbgRunLinkTxHandled = 0; self.dbgRunLinkRxIgnored = 0; self.dbgRunLinkRxHandled = 0
        self.dbgRunUnitComputes  = 0

        # Define the window size in terms of ticks
        self.dbgWinSize          = 4
        self.dbgWinPortTxIgnored = 0; self.dbgWinPortTxHandled = 0; self.dbgWinPortRxIgnored = 0; self.dbgWinPortRxHandled = 0
        self.dbgWinLinkTxIgnored = 0; self.dbgWinLinkTxHandled = 0; self.dbgWinLinkRxIgnored = 0; self.dbgWinLinkRxHandled = 0
        self.dbgWinUnitComputes  = 0

        if Network.dbgInstances > 1:
            self.error("Cannot handle more than one network for now")

    #-----------------------------------------------------------------------------------------------------------------------------
    def kill(self):                                                                                         # of Emergic.Network
        """Kill myself! Kill everything I refer to, and anything that refers to me."""

        for unit in self.dbgUnits: unit.kill()
        dbgNetworks.remove(self)
        
    #-----------------------------------------------------------------------------------------------------------------------------
    def dbgPrint(self, headers=0, network=0, units=0, ports=0, links=0, values=0):                          # of Emergic.Network
        """Print myself for debugging purposes

        headers     Specifies how (or if) attribute headers (titles) are to be printed
           =0:      Do not print a header
           =1:      Print entity names (e.g., Network, Unit, Ports/Values, Links)
           =2:      Print attribute names (e.g., RxIgnored)

        network     Specifies how (or if) network wide attributes are to be printed
            =0:     Do not print network info
            =1:     Print per tick     attributes
            =2:     Print per windowed attributes
            =3:     Print per run      attributes
        
        units       Specifies how (or if) unit attributes are to be printed
            =0:     Do not print unit info
            =1:     Print unit info
    
        ports       Specifies how (or if) port attributes are to be printed
            =0:     Do not print port info
            =1:     Print port info

        links       Specifies how (or if) link attributes are to be printed
            =0:     Do not print link info
            =1:     Print destination link info

        values      Specifies how to print current port values, if at all
            =0:     Do not print port values
            =1:     Print port value as if it was a single number (errors not idicated)
            =2:     Print port values showing low and high
        """

        if not headers and not network and not units and not links and not ports and not values:
            self.dbgPrint(headers=1, values=1); print
            self.dbgPrint(headers=2, values=1); print
            self.dbgPrint(headers=0, values=1); print
            return

        if   headers==1: print "Time ",
        elif headers==2: print "Ticks",
        elif (network == 2) and (self.time % self.dbgWinSize): return     # Not in window
        else:            print "%5d" % self.time,

        if units or ports or links or values:
            for unit in self.dbgUnits:
                unit.dbgPrint(headers, units, ports, links, values)

        if network:
            if   headers==1:
                print "%-63.63s" % ("Per " + ["Tick", "Window", "Run"][network-1] + " - - Network " + self.dbgName + " - - -"),
            elif headers==2:
                print "PTxIgn PTxHnd PRxIgn PRxHnd LTxIgn LTxHnd LRxIgn LRxHnd Compute",
            elif network==1:
                print "%6d %6d %6d %6d %6d %6d %6d %6d %6d" % (
                      self.dbgPortTxIgnored, self.dbgPortTxHandled, self.dbgPortRxIgnored, self.dbgPortRxHandled, 
                      self.dbgLinkTxIgnored, self.dbgLinkTxHandled, self.dbgLinkRxIgnored, self.dbgLinkRxHandled,
                      self.dbgUnitComputes),
            elif network==2:
                print "%6d %6d %6d %6d %6d %6d %6d %6d %6d" % (
                      self.dbgWinPortTxIgnored, self.dbgWinPortTxHandled, self.dbgWinPortRxIgnored, self.dbgWinPortRxHandled, 
                      self.dbgWinLinkTxIgnored, self.dbgWinLinkTxHandled, self.dbgWinLinkRxIgnored, self.dbgWinLinkRxHandled,
                      self.dbgWinUnitComputes),
            elif network==3:
                print "%6d %6d %6d %6d %6d %6d %6d %6d %6d" % (
                      self.dbgRunPortTxIgnored, self.dbgRunPortTxHandled, self.dbgRunPortRxIgnored, self.dbgRunPortRxHandled, 
                      self.dbgRunLinkTxIgnored, self.dbgRunLinkTxHandled, self.dbgRunLinkRxIgnored, self.dbgRunLinkRxHandled,
                      self.dbgRunUnitComputes),            

    #-----------------------------------------------------------------------------------------------------------------------------
    def dbgDumpLinks(self, dst=False):                                                                      # of Emergic.Network
        print " ID Entity..."
        print "%3d Network:    %s" % (Entity.dbgInstances.index(self), self.dbgName)
        for unit in self.dbgUnits:
            print "%3d   Unit:     %s" % (Entity.dbgInstances.index(unit), unit.dbgName)
            for port in unit.dbgPorts:
                print "%3d      Port:   %s" % (Entity.dbgInstances.index(port), port.dbgName)
                for link in port.links:
                    if not dst and (port == link.dstPort): continue     # By default, print only outgoing links.
                    print "%3d         Link: %-8.8s " % (Entity.dbgInstances.index(link), link.dbgName), 
                    if port == link.srcPort:
                        otherEndPort = link.dstPort
                        print "to:  ",
                    else:
                        otherEndPort = link.srcPort
                        print "from:",
                    print "port %-8.8s of unit %-8.8s" % (otherEndPort.dbgName, otherEndPort.unit.dbgName),
                    if link.multiplier != 1:
                        print "x%d" % link.multiplier,
                    print
                    
    #-----------------------------------------------------------------------------------------------------------------------------
    def tick(self):                                                                             # of Emergic.Network; Public
        """Update the emergic network by one time tick. Returns True if something happened."""

        something = False
        self.time += 1                              # Update current time by one tick.
        if self.dqValues():                         # Dequeue values and queue units for now or later.
            something = True
        if self.dqUnits():                          # Dequeue all units for computation. Can cause values to be queued later.
            something = True

        # Update (or reset) windowed activity counters
        if (self.time % self.dbgWinSize):
            self.dbgWinPortTxIgnored += self.dbgPortTxIgnored; self.dbgWinPortTxHandled += self.dbgPortTxHandled
            self.dbgWinPortRxIgnored += self.dbgPortRxIgnored; self.dbgWinPortRxHandled += self.dbgPortRxHandled
            self.dbgWinLinkTxIgnored += self.dbgLinkTxIgnored; self.dbgWinLinkTxHandled += self.dbgLinkTxHandled
            self.dbgWinLinkRxIgnored += self.dbgLinkRxIgnored; self.dbgWinLinkRxHandled += self.dbgLinkRxHandled
            self.dbgWinUnitComputes  += self.dbgUnitComputes
        else:
            self.dbgWinPortTxIgnored  = self.dbgPortTxIgnored; self.dbgWinPortTxHandled  = self.dbgPortTxHandled
            self.dbgWinPortRxIgnored  = self.dbgPortRxIgnored; self.dbgWinPortRxHandled  = self.dbgPortRxHandled
            self.dbgWinLinkTxIgnored  = self.dbgLinkTxIgnored; self.dbgWinLinkTxHandled  = self.dbgLinkTxHandled
            self.dbgWinLinkRxIgnored  = self.dbgLinkRxIgnored; self.dbgWinLinkRxHandled  = self.dbgLinkRxHandled
            self.dbgWinUnitComputes   = self.dbgUnitComputes

        # Update entire run activity counters and reset per tick activity counters
        self.dbgRunPortTxIgnored += self.dbgPortTxIgnored; self.dbgPortTxIgnored = 0
        self.dbgRunPortTxHandled += self.dbgPortTxHandled; self.dbgPortTxHandled = 0
        self.dbgRunPortRxIgnored += self.dbgPortRxIgnored; self.dbgPortRxIgnored = 0
        self.dbgRunPortRxHandled += self.dbgPortRxHandled; self.dbgPortRxHandled = 0
        self.dbgRunLinkTxIgnored += self.dbgLinkTxIgnored; self.dbgLinkTxIgnored = 0
        self.dbgRunLinkTxHandled += self.dbgLinkTxHandled; self.dbgLinkTxHandled = 0
        self.dbgRunLinkRxIgnored += self.dbgLinkRxIgnored; self.dbgLinkRxIgnored = 0
        self.dbgRunLinkRxHandled += self.dbgLinkRxHandled; self.dbgLinkRxHandled = 0
        self.dbgRunUnitComputes  += self.dbgUnitComputes;  self.dbgUnitComputes  = 0

        return something


    #-----------------------------------------------------------------------------------------------------------------------------
    def dqValues(self):                                                                             # of Emergic.Network; Private
        """Dequeue values from links and queue units for (now or later) computation as required.
        Returns True if something happened.
        """
        time = self.time
        something = False
        
        if time in self.qValues:                    # There are values to be dequeued at this time. If sparse change algorithm???
            for value,link in self.qValues[time]:   # Dequeue each value
                link.usage -= 1
                port = link.dstPort
                unit = port.unit
                
                if dbgTraceSched:
                    print "Getting value %f9.1 at   unit %-8.8s port %-8.8s via  link %-8.8s from unit %s" % \
                          (value.amount(), unit.dbgName, port.dbgName, link.dbgName, link.srcPort.unit.dbgName)

                # Get rxCount & rxTime parameters for ignoreRxValue() (of this computation, not since lastGot()???)
                rxCount = 0                         # Number of times value recieved since port first queued
                rxTime = 0                          # Relative time from queuing input to unit (time - eqTime)
                if unit.qTime:                      # Unit has been queued.
                    rxTime = time - unit.eqTime
                    if port.rxTimeLast >= unit.eqTime:
                        rxCount = port.rxCount
                if port.ignoreRxValue(value, rxCount, rxTime, link):    # Perhaps this link connects a fast unit to a slow unit
                    link.dbgLinkRxIgnored += 1; port.dbgLinkRxIgnored += 1; unit.dbgLinkRxIgnored += 1; self.dbgLinkRxIgnored += 1
                    if dbgTraceSched: print "Value ignored by port"
                    continue
                link.dbgLinkRxHandled += 1; port.dbgLinkRxHandled += 1; unit.dbgLinkRxHandled += 1; self.dbgLinkRxHandled += 1
                something = True
                
                qTime = time + port.iTD + unit.iTD
                if not unit.qTime:                  # Unit is idle so queue it for computations based on iTD
                    unit.qTime = qTime
                    unit.eqTime = time
                    self.qUnits.setdefault(qTime,[]).append(unit)
                    if dbgTraceSched: print "Unit %-8.8s queued for computation @ time %d." % (unit.dbgName, qTime)
                elif qTime < unit.qTime:            # Faster port needs to requeue unit
                    self.qUnits[unit.qTime].remove(unit)
                    unit.qTime = qTime
                    self.qUnits.setdefault(qTime,[]).append(unit)
                    if dbgTraceSched: print "Unit %-8.8s requeued for computation @ time %d." % (unit.dbgName, qTime)
                if not rxCount:
                    port.rxTimeFirst = time
                port.rxTimeLast = time
                port.rxCount = rxCount + 1
            del self.qValues[time]                      # Remove queue for current time
        return something

    #-----------------------------------------------------------------------------------------------------------------------------
    def dqUnits(self):                                                                              # of Emergic.Network; Private
        """Dequeue units for computation. Return True if something happened.

        Computations could cause values to be sent out, but these must traverse links with a TD>=1.
        """
        time = self.time
        something = False

        if time in self.qUnits:                     # There are units to be dequeued at this time. If sparse change algorithm???
            for unit in self.qUnits[time]:          # Dequeue each unit
                if dbgTraceSched: print "Unit %-8.8s starts to  compute." % unit.dbgName
                unit.qTime = 0                      # Indicate that unit has been dequeued
                unit.eqTime = 0
                unit.compute()
                unit.dbgUnitComputes += 1
                self.dbgUnitComputes += 1
            del self.qUnits[time]                       # Remove queue for current time
            something = True
        return something
                    
##################################################################################################################################
class Unit(Entity):
    """I am an abstract computational unit that manages change in some way.

    I interact with other units via a set of links mediated by ports.

    My derivatives will have specific change management purposes (and specific ports to define their interfaces).
    My computations consist solely of
       - getting/reading/consuming information from input  ports, and
       - setting/writing/producing information to   output ports.

    I can be analogized as a working group of neurons - more specifically, their computational body/soma.

    I am created within an emergic network.

    ??? Supposedly, new units can be created dynamically during development, and learning???
    """
    
    #-----------------------------------------------------------------------------------------------------------------------------
    def __init__(self, network, name=None, iTD=0, oTD=0):                                                       # of Emergic.Unit
        """Create an abstract computationl unit. Derivatives would perform specific computations.

        network     The emergic network I am a part of.

        name        My name for debugging purposes
          =None:    Use my network creation number as my name (by default), e.g., U1, U2, U3, ...
          else:     Use name as specifed. By convention, unit names start with an uppercase 'U'.

        iTD         My input time delay (default 0).
                    The amount of time to wait after an input arrives, before I am queued for execution.
                    If I am not queued, then the first input that arrives will determine when I am queued.
                    Change this value to affect temporal (integration) sensitive - a time constant.
                    For temporaly realist networks, this should default to 5??? (use -1 to indicate default realism??? or have profiles???)

        oTD         Output time delay (default 0). The amount of time it takes me to compute.
                    Note that even if it takes 5 ticks for me to compute, all input values are read at relative time of tick=0,
                    so that values arriving at tick=1-4 will not be processed.
                    In essence, this is equivalent to adding a constant delay to all output links.
                    However my delay is meant to be dynamic, while those of links are static.
                    For temporaly realistic networks, this should default to 3??? (use -1 to indicate default realism??? or have profiles???)
        """
        self.network        = network   # All units must be created within a network.
        network.dbgUnits.append(self)
        
        if not name: name = "U" + str(len(network.dbgUnits))
        Entity.__init__(self, name)

        if iTD < 0:
            self.error("iTD < 0")
            iTD = 0
        if oTD < 0:
            self.error("oTD < 0")
            oTD = 0

        self.dbgPorts           = []    # List of my input/output ports for debugging purposes.
                                        # Derived units will have specifically accesible ports.

        self.iTD                = iTD   # Input time delay. Allows me to handle inputs that arrive at varyying timeframes.
                                        # Can also be thought of as the amount of time it takes me to compute.
                                        # If I am unqueued, then the first input value received will determine when I become queued.
                                        # This value can change to increase or decrease temporal (integration) sensitity - time constant.
                                        # For temporally realistic networks, this should default to 5???

        self.oTD                = oTD   # Output time delay.
                                        # Technically, oTD is simply the same as increaing each link TD by a constant amount.
                                        # The difference, is a link TD is meant to be static, while a unit's could be dynamic to
                                        # handle sensitizing. Moreover, it simplifies high level timings that need not be
                                        # repeated for ever output link.

        self.qTime              = 0     # Time at which I am queued for computation.
                                        # However, 0 implies the unit is idle (not queued for execution)
        self.eqTime             = 0     # Time at which I was enqueued (the first value that arrived at this unit)
                                        # 0 implies I am not queued for execution.

        self.dbgSrcLinks        = 0     # Number of links sending  information out  of the unit
        self.dbgDstLinks        = 0     # Number of links bringing information into    the unit
    
        self.dbgLinkTxIgnored   = 0     #
        self.dbgLinkTxHandled   = 0     #
        self.dbgLinkRxIgnored   = 0     #
        self.dbgLinkRxHandled   = 0     #
        self.dbgPortTxIgnored   = 0     #
        self.dbgPortTxHandled   = 0     #
        self.dbgPortRxHandled   = 0     #
        self.dbgPortRxIgnored   = 0     #
        self.dbgUnitComputes    = 0     # Count the number of time I compute anything.

    #-----------------------------------------------------------------------------------------------------------------------------
    def compute(self):                                                                                          # of Emergic.Unit
        """My computation when dequeued.

        I am abstract, so the derivive class must override.
        """

        self.error("compute() not overridden!")

    #-----------------------------------------------------------------------------------------------------------------------------
    def dbgPrint(self, headers=0, units=0, ports=0, links=0, values=0):                                         # of Emergic.Unit
        """Print myself for debugging purposes

        headers     Specifies how (or if) attribute headers (titles) are to be printed
           =0:      Do not print a header
           =1:      Print entity names (e.g., Network, Unit, Ports/Values, Links)
           =2:      Print attribute names (e.g., RxIgnored)

        units       Specifies how (or if) unit attributes are to be printed
            =0:     Do not print unit info
            =1:     Print unit info
    
        ports       Specifies how (or if) port attributes are to be printed
            =0:     Do not print port info
            =1:     Print port info

        links       Specifies how (or if) link attributes are to be printed
            =0:     Do not print link info
            =1:     Print destination link info

        values      Specifies how to print current port values, if at all
            =0:     Do not print port values
            =1:     Print port value as if it was a single number (errors not idicated)
            =2:     Print port values showing low and high
        """

        if not headers and not units and not links and not ports and not links and not values:
            self.dbgPrint(headers=1, values=1); print
            self.dbgPrint(headers=2, values=1); print
            self.dbgPrint(headers=0, values=1); print
            return

        if ports or links or values:
            for port in self.dbgPorts:
                port.dbgPrint(headers, ports, links, values)

        if units:
            if   headers==1:
                print "%-55.55s" % ("Unit " + self.dbgName + " - - - - - -"), 
            elif headers==2:
                print "LTxIgn LTxHnd LRxIgn LRxHnd PTxIgn PTxHnd PRxIgn PRxHnd",
            else:
                print "%6d %6d %6d %6d %6d %6d %6d %6d" % (
                    self.dbgLinkTxIgnored, self.dbgLinkTxHandled, self.dbgLinkRxIgnored, self.dbgLinkRxHandled,
                    self.dbgPortTxIgnored, self.dbgPortTxHandled, self.dbgPortRxIgnored, self.dbgPortRxHandled),

##################################################################################################################################
class Port(Entity):
    """I am a unit's source or destination port - the unit's interface to another unit via links.

    I can be analogized as a set of synapses.
    Sensors/effectors (transducers) can be simply ports connected to the environment.???

    It makes sense for a source port to have multiple links to destination ports (one-to-many).
    In this case, any value sent to this port gets replicated to each destination.
    Typically, source ports need not be derived.
    However, the Unique derivative will not send duplicate values.

    It makes less sense for a destination port to have multiple links from various sources.
    In this case, one of the values could be consumed, but which one is left unspecified.
    Derivatives must handle this case. A few of them atr
       - Unique             - will ignore duplicate values received, but doesn't handle multiple values well
       - First              - Uses first value received. Note that values come in arbitrary order.
       - Sum                - Performs (non temporal/spatial) integration of all values
    """

    #-----------------------------------------------------------------------------------------------------------------------------
    def __init__(self, unit, name=None, isSingle=False, isSrc=False, isDst=False, resetValue=True, iTD=0, oTD=0):# of Emergic.Port
        """Create a unit's input or output port.

        unit        The unit to which I am attached

        name        My name for debugging purposes. Stays the same when cloned.
                    My unique name would include my unit's, e.g., U1P1, U2P1
          =None:    use my unit's port count, e.g., P1, P2, P3, ... (default)
          else:     as specified. Should always start with a capital 'P'.

        isSingle    - specify whether I must be singly linked or allow for multiple links
          =True:    I can only have a single source or destination (input or output) link attached to me.
                    When cloned, links to external groups are not duplicated.
          =False:   I allow for multiple liks attached to me.
                    Multiple output links simply distribute values to all destinations
                    Multiple input  links have a variety of behavious that should be specified by derivation.

        isSrc       Specify whether I am a source (output) port. The first link can set this instead.
          =True:    I am a link source (unit output) port.
          =False:   I an not so specified. (Default) The first link can set this instead.
  
        isDst       - specify whether I am a destination (input) port. The first link can set this instead.
          =True:    I am a link destination (unit input) port.
          =False:   I an not so specified. (Default) The first link  can set this instead.

        resetValue  Specifies whether the (destination only) ports value should be reset to None after consumed by getValue()
            =True:  Reset my value after unit consumes it via getValue()
            =False: Don't
        """
        
        network = unit.network
        network.dbgPorts        += 1
        
        self.unit               = unit
        unit.dbgPorts.append(self)
        if not name: name = "P" + str(len(unit.dbgPorts))     
        Entity.__init__(self, name)
         
        if iTD < 0:
            self.error("iTD < 0")
            iTD = 0
        if oTD < 0:
            self.error("oTD < 0")
            oTD = 0

        self.iTD                = iTD
        self.oTD                = oTD
        self.dbgIsSrc           = isSrc # Am I a source      port? Cannot be both a source or destination port simultaneously.
        self.dbgIsDst           = isDst # Am I a destination port? Cannot be both a source or destination port simultaneously.
                                        # The first link that attaches to me determines my nature.
        self.dbgIsSingle        = False # Must I be a singly linked port, or do I allow for multiple links.

        self.links              = []    # List of links connecting me to other ports.

        self.value              = None  # For a source port, this is the last value sent
                                        # For a destination port, this is the last value received (or calculated)
                                        # Do NOT access directly, but use getValue() instead.
        self.resetValue         = resetValue

        self.dbgTxTime          = -1    # The last time a values has been sent.
                                        # A source port may only send one value per computation (1 time tick).

        self.rxTimeFirst        = 0     # The first time a port receives a value (since the last computation)
                                        # a) The unit is currently idle, so this port provides the first value.
                                        # b) This is the first time for another port, in which case it's
                                        #    last time < qTime-iTD
                                        
        self.rxTimeLast         = 0     # The last time an input was received.
                                        # A destination port can receive multiple values in the same tick,
                                        # or over several ticks iff iTD>0.

        self.rxCount            = 0     # Number of times a value has been received since last computation. (Not since last accessed???)
                                        # Have a seperate counter since last consumed by getValue()???
    

        dbgSrcLinks             = 0     # Number of all outgoing  source      links.
        dbgDstLinks             = 0     # Number of all incomming destination links.

        dbgValueGot             = False # True when input value used (consumed) in a computation.
                                        # Simply to be able to detect those links/ports/units that produce values faster than they can be processed
                                        # When a new value replaces an unused one, this implies that the sender is faster than the receiver
        self.dbgLinkTxIgnored   = 0     #
        self.dbgLinkTxHandled   = 0     #
        self.dbgLinkRxIgnored   = 0     #
        self.dbgLinkRxHandled   = 0     #
        self.dbgPortTxIgnored   = 0     #
        self.dbgPortTxHandled   = 0     #
        self.dbgPortRxHandled   = 0     #
        self.dbgPortRxIgnored   = 0     #
        
    #-----------------------------------------------------------------------------------------------------------------------------
    def setValue(self, value):                                                                                  # of Emergic.Port
        """Set the value of an output port and send it to all destination ports.

        value   The value being set/sent.
                1) It will be replicated as required by each link, and
                2) each copy enqueued at appropriate times (my unit's output time delay, plus the link's time delay)
        """

        unit = self.unit
        ntwk = unit.network
        if self.dbgIsDst:
            self.error("cannot set values for destination ports")
            self.dbgPortTxIgnored += 1
            unit.dbgPortTxIgnored += 1
            ntwk.dbgPortTxIgnored += 1
            return
            
        time = ntwk.time
        if time == self.dbgTxTime:
            self.error("cannot set port values more than once per tick")
            self.dbgPortTxIgnored += 1
            unit.dbgPortTxIgnored += 1
            ntwk.dbgPortTxIgnored += 1
            return

        if self.ignoreTxValue(value):   # Derived ports may ignore values in certain cases.
            self.dbgPortTxIgnored += 1
            unit.dbgPortTxIgnored += 1
            ntwk.dbgPortTxIgnored += 1
            return

        self.dbgPortTxHandled += 1
        unit.dbgPortTxHandled += 1
        ntwk.dbgPortTxHandled += 1

        self.value = value
        self.dbgTxTime = time
 
        # Enqueue this value to all destinations.
        qCount = 0              # Number of link values queued from this port, simply to be able to increment port counters
        qValues = ntwk.qValues
        for link in self.links: # Enqueue a (tuppled) copy for each destination port
            if link.capacity and (link.usage >= link.capacity):
                link.dbgLinkTxIgnored += 1; self.dbgLinkTxIgnored += 1; unit.dbgLinkTxIgnored += 1; ntwk.dbgLinkTxIgnored += 1
                continue
            link.dbgLinkTxHandled += 1; self.dbgLinkTxHandled += 1; unit.dbgLinkTxHandled += 1; ntwk.dbgLinkTxHandled += 1
            link.usage += 1
            
            qTime = time + self.oTD + unit.oTD + link.TD
            #if qTime in qValues:        qValues[qTime].append((value,link))
            #else:                       qValues[qTime] =     [(value,link)]
            if link.multiplier ==1:
                newValue = value
            else:
                newValue = value * link.multiplier
            qValues.setdefault(qTime,[]).append((newValue,link))
            qCount+= 1
            if dbgTraceSched:
                print   "Sending value %f9.1 from unit %-8.8s port %-8.8s over link %-8.8s to   unit %s" % \
                        (value.amount(), link.srcPort.unit.dbgName, link.srcPort.dbgName, link.dbgName, link.dstPort.unit.dbgName)

        if not qCount:  # Either this port is not linked, or all its links are at capacity. Its value has not been deliverred
            self.dbgPortRxIgnored += 1; unit.dbgPortRxIgnored += 1; ntwk.dbgPortRxIgnored += 1

    #-----------------------------------------------------------------------------------------------------------------------------
    def getValue(self):                                                                                         # of Emergic.Port
        """Get a received value from an input port. None if never received.

        It is also possible to get the last sent value of an output port.
        In fact, units should not have internal state, but can expose these via unlinked output ports.

        If I have multiple input links delivering multiple values at the same time,
        all but the last may be lost, and the last is arbtrary.

        This, derivatives will correctly handle multiple values received.

        The value may be reset to None once received.

        return
            None:   If no value ever received
            else:   The last value received
        """

        self.dbgValueGot = True         # Indicate that the unit has consumed this value
        
        if not self.value: return None

        rv = self.value
        if self.resetValue and self.dbgIsDst: self.value = None
        return rv

    #-----------------------------------------------------------------------------------------------------------------------------
    def ignoreRxValue(self, value, rxCount, rxTime, link):                                          # of Emergic.Port; override
        """Should a newly received (dequeued) value be ignored by the unit so that it wont be queued for computation?

        If the unit is queued, do something smart with the value.
        Derivative ports should use this method to handle multiple received values.

        return
            True:   Ignore the recently received (dequeued) value and do not queue my unit for computation.
            False:  Handle the recently received (dequeued) value and queue my unit for computation.

        value       The recently received (dequeued) value

        rxCount     The number of times this port has previously received values (since unit queued).
        
        rxTime      The amount of time since the unit has been queued.

        link        The link from which the value arrives. ??? Get rid of this parameter ???
        """
 
        # Derivatives can manipulate the value as required (find averages, totals, maxima, etc)
        self.value = value                  # Always handle value
        return False                        # Indicate that value was handled

    #-----------------------------------------------------------------------------------------------------------------------------
    def ignoreTxValue(self, value):                                                                 # of Emergic.Port; override
        """Should the port ignore the value being sent?

        Use a more specific port type for most networks.
           
        return
            True:   Ignore the value being sent.
            False:  Send the value to all destinations.
        """

        return False                        # Indicate that value can be sent through all links

    #-----------------------------------------------------------------------------------------------------------------------------
    def dbgPrint(self, headers=0, ports=0, links=0, values=0):                                                  # of Emergic.Port
        """Print myself for debugging purposes

        headers     Specifies how (or if) attribute headers (titles) are to be printed
           =0:      Do not print a header
           =1:      Print entity names (e.g., Network, Unit, Ports/Values, Links)
           =2:      Print attribute names (e.g., RxIgnored)

        ports       Specifies how (or if) port attributes are to be printed
            =0:     Do not print port info
            =1:     Print port info

        links       Specifies how (or if) link attributes are to be printed
            =0:     Do not print link info
            =1:     Print destination link info: handled counters only
            =2:                                  ignored counters only
            =3:                                  handled and ignored counters

        values      Specifies how to print current port values, if at all
            =0:     Do not print port values
            =1:     Print port value as if it was a single number (errors not idicated)
            =2:     Print port values showing low and high
        """

        if not headers and not ports and not links and not links and not values:
            self.dbgPrint(headers=1, values=1); print
            self.dbgPrint(headers=2, values=1); print
            self.dbgPrint(headers=0, values=1); print
            return
            
        if links:
            for link in self.links:
                if link.srcPort==self: link.dbgPrint(headers, links)

        if ports:
            if   headers==1:
                print "%-55.55s" % "Port - - - " + self.dbgName + " - - -",
            elif headers==2:
                print "LTxIgn LTxHnd LRxIgn LRxHnd PTxIgn PTxHnd PRxIgn PRxHnd",
            else: # print ports
                print "%6d %6d %6d %6d %6d %6d %6d %6d" % (
                    self.dbgLinkTxIgnored, self.dbgLinkTxHandled, self.dbgLinkRxIgnored, self.dbgLinkRxHandled,
                    self.dbgPortTxIgnored, self.dbgPortTxHandled, self.dbgPortRxIgnored, self.dbgPortRxHandled),

        if values and (not self.resetValue or not self.dbgIsDst):
            if   headers==1:
                if values==1:       print "%9.9s"      % self.unit.dbgName,
                else:               print "%19.19s"    % ("Unit " + self.unit.dbgName),
            elif headers==2:
                if values==1:       print "%9.9s"      % self.dbgName,
                else:               print "%19.19s"    % ("Value " + self.dbgName),
            else: # print values
                if self.value:
                    if   values==1: print "%9d"       % self.value.amount(),
                    else:           print "%9d %9d" % (self.value.low, self.value.hgh),
                else:
                    if   values==1: print "     None",
                    else:           print "     None      None",
                    
##################################################################################################################################
class PortFirst(Port):
    """I am a port that allows for multiple inputs, but only handles the first one (for efficiency)."""
    
    #-----------------------------------------------------------------------------------------------------------------------------
    def ignoreRxValue(self, value, rxCount, rxTime, link):                                                  # of Emergic.PortFirst
        """Ignore all but the first value."""
        if rxCount > 0: return True                             # Ignore 2nd and subsequent values
        self.value = value                                      # Handle 1st value
        return False
        
##################################################################################################################################
class PortUnique(Port):
    """I am a port that only handles unique values, i.e., I ignore duplicate values received or sent.

    A duplicate value (since last send) is never sent again, so the destination port will not be enqueued for computation.
    A duplicate value (since last received) is ignored, so my unit will not be enqueued for computation.

    This should be the default port in any Change handling system.
    """

    #-----------------------------------------------------------------------------------------------------------------------------
    def ignoreRxValue(self, value, link):                                                               # of Emergic.PortUnique
        """Ignore duplicate values received. Handle unique values."""
        if self.value and (self.value == value): return True    # Ignore duplicate value
        self.value = value                                      # Handle unique value
        return False


    #-----------------------------------------------------------------------------------------------------------------------------
    def ignoreTxValue(self, value, link):                                                               # of Emergic.PortUnique
        """Ignore duplicate values sent."""
        if self.value and (self.value == value): return True    # Ignore duplicate values
        return False                                            # Send unique values

##################################################################################################################################
class PortSum(Port):
    """I am a port that sums all values received. I do temporal and spatial sumation.
    """

    #-----------------------------------------------------------------------------------------------------------------------------
    def ignoreRxValue(self, value, rxCount, rxTime, link):                                                  # of Emergic.PortSum
        """Never ignore a value, but sum them up.
        """
        if not rxCount:
            self.value = copy.copy(value)                       # It will be modified, so a fresh copy must be made
            if self.dbg: print "0: value=", self.value.amount()
        else:
            self.value += value
            #self.value.confidence   = value.confidence          #??? What to do here?
            if self.dbg: print "1: value=", self.value.amount(), "+", value.amount()
        return False;

##################################################################################################################################
class PortMaxAmount(Port):
    """I am a port that retains the value with maximum amount.
    """
    #-----------------------------------------------------------------------------------------------------------------------------
    def ignoreRxValue(self, value, rxCount, rxTime, link):                                              # of Emergic.PortMaxAmount
        if rxCount and (value.amount <= self.value.amount):
            return True                                         # Ignore smaller values beyond the first
        self.value = value
        return False

##################################################################################################################################
class PortMaxConfidence(Port):
    """I am a port that retains the value with maximum confidence.
    """
    #-----------------------------------------------------------------------------------------------------------------------------
    def ignoreRxValue(self, value, rxCount, rxTime, link):                                          # of Emergic.PortMaxConfidence
        if rxCount and (value.confidence <= self.value.confidence):
            return True                                         # Ignore smaller values beyond the first
        self.value = value
        return False

##################################################################################################################################
class Link(Entity):
    """I connect a source unit with a (possibly foreign network) destination unit (mediated by ports).

    I specify how values are transmitted from source to destination ports.
    However, I do not contain these values.
    Instead values are globally enqued based on the link TD.
    """

    #-----------------------------------------------------------------------------------------------------------------------------
    def __init__(self, srcPort, dstPort, name=None, TD=1, capacity=0, multiplier=1):                            # of Emergic.Link
        """Create myself

        srcPort     The source      port I am linking from
        
        dstPort     The destination port I am linking to

        name        My name for debugging purposes
            =None:  Use my source port name and it's link creation number, e.g., PxL1, PxL2, PxL3, ...
            else:   Use specified value. By convention, absolute link names start with an uppercase 'L'

        TD          my time delay (default of 1).
                    A link has a minimal delay of 1 to prevent infinite scheduling loops.
                    A unit may have zero iTD and oTD values.
                    My TD is meant to be static (???except perhaps during development).
                    The source unit's oTD can by dynamic and is added to my TD.
                    Together, they specify when a value is to be received at a destination port.
                    
        capacity    Number of values the link can hold at a time.
            0:      Link can hold infinite values, but this could never be more than TD as a port
                    does not allow more than one value being sent at a time.

        multiplier  The value being sent down the link is the value set for the port multiplied by this amount.
            1:      Default value.
        """

##        if not name: name = srcPort.dbgName + "L" + str(len(srcPort.links) + 1)
        if not name: name = "L" + str(len(srcPort.links) + 1)
        Entity.__init__(self, name)

        # Design debugging error checks
        if not srcPort:
            self.error("source port unspecified")
            return
        if not dstPort:
            self.error("destination port unspecified")          # ??? Allow this for growing links???
            return
        if srcPort == dstPort:
            self.error("cannot link a port to itself")  # As it can't be both source and destination!
            # Although units can link to themselves as a "kick me" to do another part of the computation.
            # This makes for a complex, state based computation that is NOT encourged - the wrong design paradigm
            return
        if srcPort.unit.network != dstPort.unit.network:
            self.error("cannot link across networks")           # ??? for now (not that multiple networks are allowed anyway...)
            return
        if srcPort.dbgIsDst:
            self.rrror("cannot link from a destination port")
            return
        if dstPort.dbgIsSrc:
            self.error("cannot link to a source port")
            return
        if srcPort.dbgIsSingle and len(srcPort.links):
            self.error("cannot link from a single valued source port that is already linked")
            return
        if dstPort.dbgIsSingle and len(dstPort.links):
            self.error("cannot link to a single valued destination port that is already linked")
            return
        if TD < 1:
            self.error("TD < 1")
            return
        if capacity < 0:
            self.error("capacity < 0")
            return
        if not multiplier:
            self.error("multiplier is 0")

        srcPort.isSrc       = True
        dstPort.isDst       = True
        self.srcPort        = srcPort
        self.dstPort        = dstPort
        self.TD             = TD
        self.capacity       = capacity
        self.usage          = 0                 # Number of values currently traversing the link (are enqueued)
        
        srcPort.links.append(self)
        dstPort.links.append(self)

        self.multiplier     = multiplier        # How much to multiply the port value before sending it down this link.

        srcPort.unit.dbgSrcLinks += 1
        dstPort.unit.dbgDstLinks += 1
        srcPort.unit.network.dbgSrcLinks += 1   # ??? Currently, source and destination networks must be the same
        dstPort.unit.network.dbgDstLinks += 1   

        self.dbgLinkTxIgnored = 0               # Number of values ignored by this link due to capacity restriction.
        self.dbgLinkTxHandled = 0               # Number of values handled (sent and queued) by this link
        self.dbgLinkRxIgnored = 0               # Number of values received but ignored by destination port of this link
        self.dbgLinkRxHandled = 0               # Number of values received and handled by destination port of this link

    #-----------------------------------------------------------------------------------------------------------------------------
    def kill(self):                                                                                             # of Emergic.Link
        """Kill me! Remove all references to and from myself."""

        port = self.dstPort
        unit = port.unit
        ntwk = unit.network
        
        # Remove all values enqueued via me
        if self.srcPort and self.usage:
            for qTime, values in self.srcPort.network.qValues.iteritems():
                if not self.usage: break
                for entry in values:
                    value, link = entry
                    if link == self:
                        values.remove(entry)
                        self.usage -= 1
                        self.dbgLinkRxIgnored += 1
                        port.dbgLinkRxIgnored += 1
                        unit.dbgLinkRxIgnored += 1
                        ntwk.dbgLinkRxIgnored += 1
                        if not self.usage: break
        
        if self.srcPort:
            self.srcPort.links.remove(self)
            self.srcPort.unit.dbgSrcLinks -= 1
            self.srcPort.unit.network.dbgSrcLinks -= 1
            self.srcPort = None
        if self.dstPort:
            self.dstPort.links.remove(self)
            self.dstPort.unit.dbgDstLinks -= 1
            self.dstPort.unit.network.dbgDstLinks -= 1
            self.dstPort = None
      
    #-----------------------------------------------------------------------------------------------------------------------------
    def dbgPrint(self, headers=0, links=0):                                                                     # of Emergic.Link
        """Print myself for debugging purposes

        headers     Specifies how (or if) attribute headers (titles) are to be printed
           =0:      Do not print a header
           =1:      Print entity names (e.g., Network, Unit, Ports/Values, Links)
           =2:      Print attribute names (e.g., RxIgnored)

        links       Specifies how (or if) link attributes are to be printed
            =0:     Do not print link info
            =1:     Print destination link info: handled counters only
            =2:                                  ignored counters only
            =3:                                  handled and ignored counters
        """

        if not headers and not links:
            self.dbgPrint(headers=1, links=3); print
            self.dbgPrint(headers=2, links=3); print
            self.dbgPrint(headers=0, links=3); print
            return;
        
        if   headers==1:
            if links==3:    print "%-27.27s"  % (self.srcPort.unit.dbgName + self.dbgName + " - - -"),
            else:           print "%-13.13s"  % (self.srcPort.unit.dbgName + self.dbgName + " -"),
        elif headers==2:
            if   links==1:  print "LTxHnd LRxHnd",
            elif links==2:  print "LTxIgn LRxIgn",
            else:           print "LTxIgn LTxHnd LRxIgn LRxHnd",   
        else:
            if   links==1:  print "%6d %6d"         % (self.dbgLinkTxHandled, self.dbgLinkRxHandled),
            elif links==2:  print "%6d %6d"         % (self.dbgLinkTxIgnored, self.dbgLinkRxIgnored),
            else:           print "%6d %6d %6d %6d" % (self.dbgLinkTxIgnored, self.dbgLinkTxHandled, self.dbgLinkRxIgnored, self.dbgLinkRxHandled),

##################################################################################################################################
class Value(Entity):
    """I am an abstract and minimally concrete computational value representing change in some aspect.
    Derivatives can increase my representation???

    I am currently implemented as "interval arithmetic". See wikipedia. I am overly conservative and lead to worst case expansion of error limits.
    Also see "Propagation of uncertainty". Probably re-implement with: Sum(S), SumSqaured(SS) & Number(N).

    I am created via a unit's computation and sent to one of its ports.
    The port has numerous links to other units, so I will be cloned and queued for reception to each unit.
    I can be read by all the destination units when delivered.

    Multiple values can be sent down a link, and if the destination unit is slow, some values could be lost!

    If a unit has an iTD=0, then I am not required, as separate ports could handle the amount/confidence pairs.
    However, with an iTD>0, finding a max amount or max confidence is not possible.

    ??? Need to define confidence (absolute, percent), significance, standard error, etc.

    ??? Would like to define numeric range as -+ 0.000 - 128.0
    ??? All numbers logarithmic?
    ??? For now, assume confidence is absolute +- error, so that completely guesee of zero is stil +- 65535
    value = (low, hgh) where abs(value) = (low+hgh)/2

    Unlike classical ANNs, my values are usefull
    """

    # This fuzzy value is optimized for addition and subtraction (which is the only thing that should be done!)

    MinMaxAmount = 2**16                # The absolute minimum and maximum values the system allows.
                                        # Precise     0:    (0,0)
                                        # Imprecise   0:    (-MinMaxAmount, +MinMaxAmount)
                                        # Precise   max:    (+MinMaxAmount, +MinMaxAmount)
                                        # Imprecise max:    (0, 2*MinMaxAmount)

    #-----------------------------------------------------------------------------------------------------------------------------
    def Amount_Confidence(amount=0.0, confidence=0.0):                                                          # of Emergic.Value
        """Create a Value given an Amount and Confidence""" 
        return Amount_ErrAbs(amount, MinMaxAmount*(1-confidence))
    Amount_Confidence = staticmethod(Amount_Confidence)    

    #-----------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def Amount_ErrPcnt(amount=0.0, err=100.0):                                                                  # of Emergic.Value
        """Create a Value give an Amount and an Error expressed in percent.

        This is likely the best for a sensory input.
        """
        return Value(amount * (1 - err/100), amount * (1 + err/100))

    #-----------------------------------------------------------------------------------------------------------------------------
    def Amount_ErrAbs(amount=0.0, err=MinMaxAmount):                                                            # of Emergic.Value
        """Create a Value given an amount an an Error expressed in absolute (+-) terms.
        """
        return Value(amount-err, amount+err)
    Amount_ErrAbs = staticmethod(Amount_ErrAbs)    

    #-----------------------------------------------------------------------------------------------------------------------------
    def __init__(self, low=-MinMaxAmount, hgh=MinMaxAmount):                                                    # of Emergic.Value
        """Construct a Value. By defaults it is a most uncertain zero."""
        if (low > hgh):
            print "low > high"
            self.low = hgh
            self.hgh = low
        else:
            self.low    = low
            self.hgh    = hgh

    #-----------------------------------------------------------------------------------------------------------------------------
    def __str__(self):                                                                                          # of Emergic.Value
        return str(self.amount()) + "+-" + str(self.errAbs())

    #-----------------------------------------------------------------------------------------------------------------------------
    def __repr__(self):                                                                                         # of Emergic.Value
        return "Emergic.Value(" + str(self.low) + "," + str(self.hgh) + ")"

    #-----------------------------------------------------------------------------------------------------------------------------
    def amount(self):                                                                                           # of Emergic.Value
        return (self.low + self.hgh) / 2

    #-----------------------------------------------------------------------------------------------------------------------------
    def errAbs(self):                                                                                           # of Emergic.Value
        return (self.hgh - self.low) / 2

    #-----------------------------------------------------------------------------------------------------------------------------
    def errPcnt(self):                                                                                          # of Emergic.Value
        return abs(100.0 * (self.hgh - self.low) / (self.low + self.hgh))

    #-----------------------------------------------------------------------------------------------------------------------------
    def __abs__(self):                                                                                          # of Emergic.Value
        return abs(self.amount())
    
    #-----------------------------------------------------------------------------------------------------------------------------
    def __neg__(self):                                                                                          # of Emergic.Value
        return Value(-self.hgh, -self.low)
    
    #-----------------------------------------------------------------------------------------------------------------------------
    def __add__(self, other):                                                                                   # of Emergic.Value
        if isinstance(other, int) or isinstance(other, float):
            return Value(self.low+other, self.hgh+other)
        low = self.low + other.low
        hgh = self.hgh + other.hgh
        #if low<=hgh: return Value(low,hgh)
        return Value(low,hgh)

    #-----------------------------------------------------------------------------------------------------------------------------
    def __iadd__(self, other):                                                                                  # of Emergic.Value
        """Increment my contents. Take care - most clients pass values by reference, so you may need to make a private copy!
        """
        if isinstance(other, int) or isinstance(other, float):
            self.low += other; self.hgh += other
            return self
        self.low += other.low
        self.hgh += other.hgh
        return self

    #-----------------------------------------------------------------------------------------------------------------------------
    def __sub__(self, other):                                                                                   # of Emergic.Value
        if isinstance(other, int) or isinstance(other, float):
            return Value(self.low-other, self.hgh-other)
        low = self.low - other.hgh
        hgh = self.hgh - other.low
        #if low<=hgh: return Value(low,hgh)
        return Value(low,hgh)

    #-----------------------------------------------------------------------------------------------------------------------------
    def __cmp__(self, other):                                                                                   # of Emergic.Value
        """Fuzzy comparison (-1, 0, +1)."""
        if isinstance(other, int) or isinstance(other, float):
            if self.hgh < other: return -1
            if self.low > other: return +1
            return 0
        if self.hgh < other.low: return -1
        if self.low > other.hgh: return +1
        return 0                        # we overlap

    #-----------------------------------------------------------------------------------------------------------------------------
    def __lt__(self, other):                                                                                    # of Emergic.Value
        """Am I absolutely less than the other?"""
        if isinstance(other, int) or isinstance(other, float):
            return self.hgh < other
        return self.hgh < other.low

    #-----------------------------------------------------------------------------------------------------------------------------
    #def __eq__(self, other):           # Will use __cmp__ by default
    #    return self.amount == other.amount

    #-----------------------------------------------------------------------------------------------------------------------------
    def __mul__(self, other):                                                                                   # of Emergic.Value
        """Returns x * y where y is either of type Emergic.Value or int. Note that midpoints are not presrved!"""
        if isinstance(other, int) or isinstance(other, long) or isinstance(other, float):
            if other >= 0:
                return Value(self.low * other, self.hgh * other)
            return     Value(self.hgh * other, self.low * other)
        
        if self.low >= 0:
            if other.low >= 0:  return Value(self.low * other.low, self.hgh * other.hgh) # ( 3  5) * ( 7  9) => ( 21  45)
            if other.hgh <= 0:  return Value(self.hgh * other.low, self.low * other.hgh) # ( 3  5) * (-9 -7) => (-45 -21)
            return                     Value(self.hgh * other.low, self.hgh * other.hgh) # ( 3  5) * (-7  9) => (-35  45) or; note that self.low unused!
                                                                                         # ( 3  5) * (-9  7) => (-45  35)
        if self.hgh <= 0:
            if other.low >= 0:  return Value(self.low * other.hgh, self.hgh * other.low) # (-5 -3) * ( 7  9) => (-45 -21)
            if other.hgh <= 0:  return Value(self.hgh * other.hgh, self.low * other.low) # (-5 -3) * (-9 -7) => ( 21  45)
            return                     Value(self.low * other.hgh, self.low * other.low) # (-5 -3) * (-7  9) => (-45  21) or; note that self.hgh unused!
                                                                                         # (-5 -3) * (-9  7) => (-35  45)
        if     other.low >= 0:  return Value(self.low * other.hgh, self.hgh * other.hgh) # (-3  5) * ( 7  9) => (-27  45) or; note that other.low unused!
                                                                                         # (-5  3) * ( 7  9) => (-45  27)
        if     other.hgh <= 0:  return Value(self.hgh * other.low, self.low * other.low) # (-3  5) * (-9 -7) => (-45  27) or; note that other.hgh unused
                                                                                         # (-5  3) * (-9 -7) => (-27  45)

        return Value(min(self.low*other.hgh, self.hgh*other.low), max(self.low*other.low, self.hgh*other.hgh))

    #-----------------------------------------------------------------------------------------------------------------------------
    def __div__(self, other):                                                                                   # of Emergic.Value
        """returns x / y where y is either of type Emergic.Value or int"""
        if isinstance(other, int) or isinstance(other, float):
            if other >= 0:
                return Value(self.low / other, self.hgh / other)
            return     Value(self.hgh / other, self.low / other)
        return None     # Not yet implemented!

    #-----------------------------------------------------------------------------------------------------------------------------
    def setConfidence(confidence=0.0):                                                                          # of Emergic.Value
        """Set my confidence in the amount.

        confidence  The confidence in the amaount.
            0.0:    No confidence (default) - widest possible error bars
            1.0:    Compolete confidence    - no error bars
        """
        amount = self.amount()
        err = MinMaxAmount * (1.0 - confidence)

        if amount >= 0:
            self.low = amount - err
            self.hgh = amount + err
        else:
            self.low = amount + err
            self.hgh = amount - err

