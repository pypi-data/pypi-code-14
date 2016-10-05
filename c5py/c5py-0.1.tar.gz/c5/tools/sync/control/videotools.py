import os.path
import subprocess
import dataanalysis


def prepare_videos(file_names, destination, rawcopy):
    destination = destination
    if len(file_names) == 1 and os.path.basename(file_names[0]).split(".")[1] == "mp4":
        cmd = ["ln -s %s %s" % (os.path.abspath(file_names[0]), destination)]
    else:
        files = ""
        for filename in file_names:
            if os.path.exists(filename) is True:
                files+=" "+filename
        cmd = ["cat %s | ffmpeg -preset slow -i - -r 25 -y %s -vcodec x264" % (files, destination)]
    print cmd
    job = subprocess.Popen(cmd,shell=True)
    exitcode = job.wait()
    if exitcode != 0:
        return False
    return True


def get_syncs(file_name):
    events = dataanalysis.VisualAnalysis.detect_sync(file_name)
    return events


def create_images(file_path, destination, width, height):
    file_name = os.path.basename(file_path)
    cmd = ["ffmpeg", "-i", file_path, "%s/%s.\%d.png" % (destination, file_name)]
    print cmd
    subprocess.call(cmd)

