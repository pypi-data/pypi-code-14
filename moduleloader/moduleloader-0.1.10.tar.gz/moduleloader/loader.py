import sys
import inspect
import os

class RelativePath:

    def __init__(self, relativePath,modules=[]):
        frame = inspect.stack()[1]
        path = os.path.join(os.path.join(os.path.dirname(frame[1]),relativePath))
        if not modules:
            for root, dirs, files in os.walk(path):
                sys.path.append(root)
        else:
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file in modules:
                        if not root in sys.path:
                            sys.path.append(root)
                        modules.pop(modules.index(file))

        if modules:
            for module in modules:
                print("no process module", module)
