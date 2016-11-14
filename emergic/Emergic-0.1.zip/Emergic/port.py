"""
I define a port through which values are sent or received from one computational unit to another in an Emergic Network.

Author: David Pierre Leibovitz (C) 2008-2010
"""

from entity     import Entity           # Common (hierarchical named) debugging support
from network    import dbgTraceSched    # Determine whether scheduling should be traced.

from copy       import deepcopy         # All values within the emergic system are sent by (copied) value, not by reference

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
          =False:   I allow for multiple links attached to me.
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
        self.dbgIsSingle        = isSingle # Must I be a singly linked port, or do I allow for multiple links.

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
    def kill(self):
        "Kill myself and everything I refer to (and everything that refers to me"
        unit = self.unit
        network = unit.network
        for link in self.links[:]: link.kill()
        unit.dbgPorts.remove(self)
        network.dbgPorts -= 1
        self.unit       = None
        self.value      = None
        self.network    = None
        self.links      = None
        Entity.kill(self)
    #-----------------------------------------------------------------------------------------------------------------------------
    def setValue(self, value):
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

        self.value = deepcopy(value)   # As originally provided (not scaled or otherwise manipulated)
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
            newValue = self.value
            if not (link.multiplier == 1):
                newValue = newValue * link.multiplier     # Or call an abstract method?
            newValue = self.linkDependentValue(newValue, link)
            qValues.setdefault(qTime,[]).append((newValue,link))
            qCount+= 1
            if dbgTraceSched:
                print   "Sending value %-9.9s from unit %-8.8s port %-8.8s over link %-8.8s to   unit %s" % \
                        (str(newValue), link.srcPort.unit.dbgName, link.srcPort.dbgName, link.dbgName, link.dstPort.unit.dbgName)

        if not qCount:  # Either this port is not linked, or all its links are at capacity. Its value has not been deliverred
            self.dbgPortRxIgnored += 1; unit.dbgPortRxIgnored += 1; ntwk.dbgPortRxIgnored += 1

    #-----------------------------------------------------------------------------------------------------------------------------
    def linkDependentValue(self, value, link):
        """Allow derivatives to modify the value in a link dependent way"""
        return value
    #-----------------------------------------------------------------------------------------------------------------------------
    def getValue(self):
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
        
        if self.value is None: return None

        if self.resetValue and self.dbgIsDst:
            rv          = deepcopy(self.value)
            self.value  = None
        else:
            rv          = deepcopy(self.value)
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
            #self.value = copy.copy(value)                       # It will be modified, so a fresh copy must be made !!! All values are now deepcopies!
            self.value = value
            if self.dbg: print "0: value=", repr(value)
        else:
            self.value += value
            #self.value.confidence   = value.confidence          #??? What to do here?
            if self.dbg: print "1: value=", repr(self.value), "+", repr(value)
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
