"""
I define a temporal link from the output/source port of a computational unit, to the input/destination port of another.

Author: David Pierre Leibovitz (C) 2008-2010
"""

from entity import Entity       # Common (hierarchical named) debugging support

##################################################################################################################################
class Link(Entity):
    """I connect a source unit with a (possibly foreign network) destination unit (mediated by ports).

    I specify how values are transmitted from source to destination ports.
    However, I do not contain these values.
    Instead values are globally enqued based on the link TD.
    """

    #-----------------------------------------------------------------------------------------------------------------------------
    def __init__(self, srcPort, dstPort, name=None, TD=1, capacity=0, multiplier=1):
        """Create myself

        srcPort     The source      port I am linking from
        
        dstPort     The destination port I am linking to

        name        My name for debugging purposes
            =None:  Use my source port name and it's link creation number, e.g., PxL1, PxL2, PxL3, ...
            else:   Use specified value. By convention, absolute link names start with an uppercase 'L'

        TD          my time delay (default of 1).
                    A link has a minimal delay of 1 to prevent infinite scheduling loops.
                    ### Not Yet Implemented ### WARNING: ONLY ENVIRONMENTAL LINKS CAN HAVE TD==0.
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
            self.error("cannot link from a destination port")
            return
        if dstPort.dbgIsSrc:
            self.error("cannot link to a source port")
            return
        if srcPort.dbgIsSingle and len(srcPort.links):
            self.error("cannot link from a single valued source port that is already linked")
            return
        if dstPort.dbgIsSingle and len(dstPort.links):
            self.error("cannot link to a single valued destination port that is already linked")
            #raise "cannot link to a single valued destination port that is already linked"
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
            for qTime, values in self.srcPort.unit.network.qValues.iteritems():
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
        Entity.kill(self)
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

