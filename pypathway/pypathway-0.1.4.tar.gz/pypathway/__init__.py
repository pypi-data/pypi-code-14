import sys

# the interfaces core object exposes to users
if sys.version[0] == "2":
    from core.SBGNPDImpl.objects import SBGNParser
    from core.GPMLImpl.objects import GPMLParser
    from core.KEGGImpl.objects import KEGGParser
    from core.BioPAXImpl.objects import BioPAXParser

    # the interface database query expose to users
    from query.database import PublicDatabase
    from query.common import PathwayFormat, SupportedDatabase
    from visualize.options import *
    from query.network import *
else:
    from .core.SBGNPDImpl.objects import SBGNParser
    from .core.GPMLImpl.objects import GPMLParser
    from .core.KEGGImpl.objects import KEGGParser
    from .core.BioPAXImpl.objects import BioPAXParser

    # the interface database query expose to users
    from .query.database import PublicDatabase
    from .query.common import PathwayFormat, SupportedDatabase
    from .visualize.options import *
    from .query.network import *

def version():
    return "0.10.2"

