import sys
import site
import os
for s in site.getsitepackages():
    p = os.path.join(s, 'SeasObjects')
    if os.path.isdir(p):
        sys.path.append(p)
        break
