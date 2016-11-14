"""
I define a computational Unit of an Emergic Network.

Author: David Pierre Leibovitz (C) 2008-2010
"""

from entity import Entity       # Common (hierarchical named) debugging support
                        
##################################################################################################################################
class Unit(Entity):
    """I am an abstract computational unit that manages change in some way.

    I interact with other units via a set of links mediated by ports.

    My derivatives will have specific change management purposes (and specific ports to define their interfaces).
    My computations consist solely of
       - getting/reading/consuming information from input  ports, and
       - setting/writing/producing information to   output ports.

    I can be analogized as a working group (or pool) of neurons - more specifically, their computational body/soma.

    I am created within an emergic network.

    ??? Supposedly, new units can be created dynamically during development, and learning???
    """
    
    #-----------------------------------------------------------------------------------------------------------------------------
    def __init__(self, network, name=None, iTD=0, oTD=0):
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
        self.dbgUnitComputes    = 0     # Count the number of times I compute anything.

    #-----------------------------------------------------------------------------------------------------------------------------
    def kill(self):
        "Kill myself and everything I refer to (and everything that refers to me"
        for port in self.dbgPorts[:]: port.kill()
        self.network.dbgUnits.remove(self)
        if self.qTime: self.network.qUnits[self.qTime].remove(self)
        self.network    = None
        self.dbgPorts   = None
        Entity.kill(self)
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
