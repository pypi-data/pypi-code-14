"""
I define a common debugging root class for all entities in the emergic system.

(C) 2008-2010 David Pierre Leibovitz
"""

##################################################################################################################################
class Entity(object):
    """
    I am the supermost ancestral derivational object for all entities in the emergic module.

    I am used for common debugging purposes only.
    """
    #-----------------------------------------------------------------------------------------------------------------------------
    #dbgInstances = []   # A quick debugging access to all Entities. See network.dbgDumpLinks().
    dbgInstances    = 0    # Number of instances of this classs
    #-----------------------------------------------------------------------------------------------------------------------------
    def __init__(self, name):
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
        #Entity.dbgInstances.append(self)
        Entity.dbgInstances += 1
    #-----------------------------------------------------------------------------------------------------------------------------
    def kill(self):
        "Kill myself and everything I refer to (and everything that refers to me"
        #Entity.dbgInstances.remove(self)
        Entity.dbgInstances -= 1
        self.dbgName = None
    #-----------------------------------------------------------------------------------------------------------------------------
    def error(self, text):
        """Print an error message with respect to this entity."""
        print("Error (" + self.dbgName + "): " + text)

