"""
I define a message Value that is transmitted across a Link from the source Port of a computational Unit, to the destination port of another in an Emergic Network.

Author: David Pierre Leibovitz (C) 2008-2010
"""

#from entity import Entity
    
##################################################################################################################################
class Value():#(Entity):        # Derive off Entity???
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
    def __radd__(self, other):
        return self.__add__(other)

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
    def __rsub__(self, other):
        return (self*-1).__add__(other)

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
    def __rmul__(self, other):
        return self.__mul__(other)

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

