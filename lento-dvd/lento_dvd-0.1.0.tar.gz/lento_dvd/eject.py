import subprocess

def eject(cdspeed=None):
    args = []
    if cdspeed is not None:
        args += ["--cdspeed", str(cdspeed)]

    subprocess.check_call(["eject"] + args)
