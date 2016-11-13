import os
import wxversion

# remove conficts beetween IM and wx
if 'GTK_IM_MODULE' in os.environ:
    del os.environ['GTK_IM_MODULE']

wxversion.select('3.0')


import beatle
appInstance = beatle.app.proCxx(0)
appInstance.MainLoop()
