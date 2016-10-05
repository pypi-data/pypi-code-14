# -*- coding: utf-8 -*-
import os.path
import subprocess

from ..config import ConfigLoader, RAW_PATH, VOL_PATH, TRIALS

def fix_check(raw, vol, tmp, trial):
    cfg = os.path.exists("%s/trial%d.json" % (vol, trial))
    if cfg:
        print "found config"
    zlib = os.path.exists("%s/trial%d_kinect.zlib" % (raw, trial))
    if zlib:
        print "found zlib kinect"
    cam3 = os.path.exists("%s/trial%d_cam3.mp4" % (vol, trial))
    if cam3:
        print "found cam3"
    cam3_small = os.path.exists("%s/trial%d_cam3_small.mpg" % (tmp, trial))
    if cam3_small:
        print "found cropped cam3"
    return (cfg and zlib and (cam3 or cam3_small))


def prepare_fix(path, trial, out="."):
    if os.path.exists("%s/trial%d_cam3_small.mpg" % (out, trial)):
        return
    call = ["cp", "%s/trial%d.json" % (path, trial), out]
    subprocess.Popen(call)
    call = ["cp", "%s/trial%d_kinect.zlib" % (path, trial), out]
    subprocess.Popen(call)
    call = ["ffmpeg", "-i", "%s/trial%d_cam3.mp4" % (path, trial), "-vf",
            "scale=320:240", "%s/trial%d_cam3_small.mpg" % (out, trial)]
    #print " ".join(call)
    subprocess.call(call)


def fix_kinect_ts(raw, vol, tmp, trial):
    if os.path.exists("%s/trial%d_kinect.c5k" % (raw, trial)):
        print "c5k file exists for trial %d. skip..." % trial
        return
    config = ConfigLoader()
    config.load("%s/trial%d.json" % (vol, trial))
    cam3_start = config.get("cam3.start")
    prepare_fix(vol, trial, tmp)
    call = ["/Users/alneuman/Workspace/riker/build/bin/kinect_fix",
            "%s/trial%d_kinect.zlib" % (raw, trial),
            "%s/trial%d_cam3_small.mpg" % (tmp, trial), str(cam3_start),
            "%s/trial%d_kinect.c5k" % (raw, trial)]
    print " ".join(call)
    subprocess.call(call)


def c5k2png(path, trial, out="."):
    config = ConfigLoader()
    config.load("%s/trial%d.json" % (path, trial))
    for phase in ["negotiation", "presentation", "free"]:
        if os.path.exists("%s/trial%d_kinect_%s" % (out, trial, phase)):
            print "Phase folder already exists! skipping..."
            continue
        phase_start = config.get("trial.phase.%s.start" % phase)
        phase_stop = config.get("trial.phase.%s.stop" % phase)
        call = ["/Users/alneuman/Workspace/riker/build/bin/c5k2png",
                "%s/trial%d_kinect.c5k" % (path, trial), str(phase_start),
                str(phase_stop), "%s/trial%d_kinect_%s" % (out, trial, phase)]
        print " ".join(call)
        p = subprocess.Popen(call, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = p.stdout.read()
        print output
        if p.poll() != 0:
            return p.returncode
#        phase_path = "%s/trial%d_kinect_%s" % (out, trial, phase)
#        for f in os.listdir(phase_path):
#            if f.endswith(".png"):
#                p = subprocess.Popen(["optipng", "%s/%s" % (phase_path, f)],
#                                     stdin=subprocess.PIPE,
#                                     stdout=subprocess.PIPE,
#                                     stderr=subprocess.STDOUT)
#                output = p.stdout.read()
#                print output
#                if p.poll() != 0:
#                    return p.returncode
    return 0


def main():
    TMP_PATH = "/Users/alneuman/tmp"

    for study, trials in TRIALS.items():
        for trial in trials:
            raw = "%s/%s/trial%d" % (RAW_PATH, study, trial)
            vol = "%s/%s/trial%d" % (VOL_PATH, study, trial)
            print "check if c5k file already exists in %s" % raw
            c5k_path = "%s/trial%d_kinect.c5k" % (raw, trial)
            if os.path.exists(c5k_path) is False:
                print "check for required resources"
                if fix_check(raw, vol, TMP_PATH, trial) is True:
                    print "fixing kinect data for trial %d" % trial
                    fix_kinect_ts(raw, vol, TMP_PATH, trial)
                else:
                    print "not all necessary data available!"
                    break
            print "convert c5k into png files"
            res = c5k2png(raw, trial, vol)
            if res != 0:
                print "error: could not convert images"
                print res
                return

if __name__ == "__main__":
    main()
