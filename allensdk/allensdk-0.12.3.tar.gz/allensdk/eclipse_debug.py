import sys
sys.path.append(
    r'/local1/eclipse/plugins/org.python.pydev_5.0.0.201605051159/pysrc')

import pydevd
pydevd.settrace(stdoutToServer=True, stderrToServer=True)
