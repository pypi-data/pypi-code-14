"""
I define an emergic network - a dynamic, temporal (message based) & highly recurrent systems made up of computational unitslinked together via their ports.

Author: David Pierre Leibovitz (C) 2008-2010
"""

dbgTraceSched = False           # Determine whether scheduling should be traced.

from entity import Entity       # Common (hierarchical named) debugging support
    
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
                                    # When all units for the current time have been dequeued, the entire dictionary entry is deleted.

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
        self.dbgLinkTxIgnored       = 0 # Global number of values not queued for transmission through links (many links per port)
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
        "Kill myself and everything I refer to (and everything that refers to me"

        # Empty queues first, as this would take a long time otherwise.
        self.qValues        = {}
        self.qUnits         = {}

        for unit in self.dbgUnits[:]: unit.kill()
        Network.dbgInstances -= 1
        self.dbgUnits       = None
        self.qValues        = None
        self.qUnits         = None
        Entity.kill(self)
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
            =1:     Print port value as if it was a single number (errors not indicated)
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

##    #-----------------------------------------------------------------------------------------------------------------------------
##    def dbgDumpLinks(self, dst=False): # ??? Convert to another form. Getting rid of Entity.dbgInstances
##        print " ID Entity..."
##        #print "%3d Network:    %s" % (Entity.dbgInstances.index(self), self.dbgName)
##        unitNum = 0
##        for unit in self.dbgUnits:
##            print "%3d   Unit:     %s" % (unitNum, unit.dbgName)
##            for port in unit.dbgPorts:
##                print "%3d      Port:   %s" % (Entity.dbgInstances.index(port), port.dbgName)
##                for link in port.links:
##                    if not dst and (port == link.dstPort): continue     # By default, print only outgoing links.
##                    print "%3d         Link: %-8.8s " % (Entity.dbgInstances.index(link), link.dbgName), 
##                    if port == link.srcPort:
##                        otherEndPort = link.dstPort
##                        print "to:  ",
##                    else:
##                        otherEndPort = link.srcPort
##                        print "from:",
##                    print "port %-8.8s of unit %-8.8s" % (otherEndPort.dbgName, otherEndPort.unit.dbgName),
##                    if link.multiplier != 1:
##                        print "x%d" % link.multiplier,
##                    print
                    
    #-----------------------------------------------------------------------------------------------------------------------------
    def tick(self):                                                                             # of Emergic.Network; Public
        """Update the emergic network by one time tick. Returns True if something happened."""

        self.dbgPortTxIgnored = 0; self.dbgPortTxHandled = 0; self.dbgPortRxIgnored = 0; self.dbgPortRxHandled = 0
        self.dbgLinkTxIgnored = 0; self.dbgLinkTxHandled = 0; self.dbgLinkRxIgnored = 0; self.dbgLinkRxHandled = 0
        self.dbgUnitComputes  = 0

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
        self.dbgRunPortTxIgnored += self.dbgPortTxIgnored
        self.dbgRunPortTxHandled += self.dbgPortTxHandled
        self.dbgRunPortRxIgnored += self.dbgPortRxIgnored
        self.dbgRunPortRxHandled += self.dbgPortRxHandled
        self.dbgRunLinkTxIgnored += self.dbgLinkTxIgnored
        self.dbgRunLinkTxHandled += self.dbgLinkTxHandled
        self.dbgRunLinkRxIgnored += self.dbgLinkRxIgnored
        self.dbgRunLinkRxHandled += self.dbgLinkRxHandled
        self.dbgRunUnitComputes  += self.dbgUnitComputes

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
# Test the Emergic Network
##################################################################################################################################
if __name__ == "__main__":
    import Emergic
    #Emergic.network.dbgTraceSched = True
    def _test():
        class TestUnit(Emergic.Unit):
            def __init__(self, n, name):
                Emergic.Unit.__init__(self,n, name)
                self.pi = Emergic.Port(self, name+"I", isDst=True)
                self.po = Emergic.Port(self, name+"O", isSrc=True)
            def compute(self):
                v = self.pi.getValue()
                self.po.setValue(v)
        n = Emergic.Network()
        u1 = TestUnit(n, name="U1")
        u2 = TestUnit(n, name="U2")
        u3 = TestUnit(n, name="U3")
        Emergic.Link(u1.po, u2.pi, name="L1")
        Emergic.Link(u1.po, u3.pi, name="L2", TD=3)

        n.dbgPrint(headers=1, values=1); print
        n.dbgPrint(headers=2, values=1); print
        n.dbgPrint(headers=0, values=1); print  # Time=0

        for t in range(0,9):
            u1.po.setValue(Emergic.Value(t,t))
            if n.tick():
                n.dbgPrint(headers=0, values=1); print
            
    _test()
