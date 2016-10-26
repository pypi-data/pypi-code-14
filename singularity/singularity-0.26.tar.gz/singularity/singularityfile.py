#!/usr/bin/env python

'''
convert.py: part of singularity package

'''

from singularity.runscript import get_runscript_parameters
from singularity.utils import zip_up, read_file
import tempfile
import tarfile
import hashlib
import zipfile
import json
import os


def from_dockerfile(dockerfile,output_folder=None,disttype="debian"):
    '''from_dockerfile will convert a Dockerfile to a Singularityfile file
    :param dockerfile: full path to the dockerfile to convert
    :param disttype: the distribution type, default is debian
    :param output_folder: the output directory for the file (optional).

    ::note

        DistType "debian"
        MirrorURL "http://ftp.us.debian.org/debian/"
        OSVersion "jessie"

        Setup
        Bootstrap

        InstallPkgs vim

        Cleanup
    '''

    tmptar = S.export(image_path=image_path,pipe=False)
    tar = tarfile.open(tmptar)
    members = tar.getmembers()
    image_name = os.path.basename(image_path)
    zip_name = "%s.zip" %(image_name.replace(" ","_"))

    # Include the image in the package?
    if remove_image:
       to_package = dict()
    else:
       to_package = {image_name:image_path}

    # Package the image with an md5 sum as VERSION
    version = get_image_hash(image_path)
    to_package["VERSION"] = version

    # Look for runscript
    if runscript == True:
        try:
            runscript_member = tar.getmember("./singularity")
            runscript_file = tar.extractfile("./singularity")
            runscript = runscript_file.read()
            to_package["runscript"] = runscript
            print("Found runscript!")

            # Try to extract input args, only python supported, will return None otherwise
            params_json = get_runscript_parameters(runscript=runscript,
                                                   name=image_name,
                                                   version=version)
            if params_json != None:
                print('Extracted runscript params!')
                to_package['%s.json' %(image_name)] = params_json

        except KeyError:
            print("No runscript found in image!")
        
    if software == True:
        print("Adding software list to package!")
        files = [x.path for x in members if x.isfile()]
        folders = [x.path for x in members if x.isdir()]
        to_package["files.txt"] = files
        to_package["folders.txt"] = folders

    # Do zip up here - let's start with basic structures
    zipfile = zip_up(to_package,zip_name=zip_name,output_folder=output_folder)
    print("Package created at %s" %(zipfile))

    # return package to user
    return zipfile

