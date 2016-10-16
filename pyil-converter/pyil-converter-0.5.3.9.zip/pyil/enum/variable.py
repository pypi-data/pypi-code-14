from getpass import getuser as __gu
import os as __os
import multiprocessing as __mp
true = True
"""Just the value True without caps."""
false = False
"""Just the value False without caps."""
locked=True
"""Values for pyil.shared.LockVar's parameter "state"."""
unlocked=False
"""Values for pyil.shared.LockVar's parameter "state"."""
common_path=[r'C:\Program Files',r'C:\Program Files (x86)', __os.path.join(r'C:\Users', __gu())]
"""The paths where files are likely to be found."""
cpu_count=__mp.cpu_count()
"""The number of cpu(cores) your computer have."""


def auto_process(length, current=cpu_count+1):
    """Pass it to pyil.shared.threading.map
    function to let it decide how many process
    best fit your computer."""
    return auto_process(length,current=current-1)if length%current<current/2else current
pythonPath=r'C:\Users\ryan_\AppData\Local\Programs\Python\Python35\python.exe'
pythonPath2=r'C:\Users\ryan_\AppData\Local\Programs\Python\Python35\pythonw.exe'

