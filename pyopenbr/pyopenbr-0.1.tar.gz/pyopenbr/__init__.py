import os
import platform
import shlex
import random
import string
import csv
from subprocess import Popen, PIPE

# Copyright 2016 Antonios Katzourakis
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

print_errors = True
open_br_executable = ''

def run(output = None, *br_args, **k_br_args):
    # Run OpenBR with the specified parameters. All the Command Line Tool API can be found at: http://openbiometrics.org/docs/api_docs/cl_api/
    br_executable = _checkForOpenBRCommandLineTool()
    
    outputPath = output
    
    if output == None:
        outputPath = _getTempPath() + ".csv"
    else:
        if output.startswith("-"):
            br_args = tuple(list(br_args) + [output])
            output = None
            outputPath = _getTempPath() + ".csv"

    if os.path.isdir(outputPath):
        raise Exception("Invalid output path. Must be a valid file path.")

    br_args = list(br_args)
    keyed_args = []
    for k in k_br_args.keys():
        keyed_args.append('-{} {}'.format(k, k_br_args[k]))

    br_args = _prioritize_args(keyed_args + br_args, outputPath)
    br_args = [br_executable] + br_args

    commd = shlex.split(" ".join(br_args))
    process = Popen(commd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    stdout = stdout.decode("utf-8").replace("\n","")
    stderr = stderr.decode("utf-8").replace("\n","")

    if print_errors:
        if stderr != '': print(stderr)
        pass

    br_output = stdout

    with open(outputPath) as f:
        if outputPath.endswith(".csv"):
            readerData = csv.DictReader(f)
            csvData = {}
            for row in readerData:
                csvData.update(row)
        
            del(csvData['File'])
            br_output = csvData
        else:
            br_output = f.read()

    if output == None:
        os.remove(outputPath)

    return br_output

def setExecutable(path):
    # Set custom path for the executable
    if os.path.isfile(path):
        open_br_executable = path

    raise Exception("Invalid Path: The Path doesn't point to a valid file.")

def disableErrors():
    # Disable error logging in the console
    print_errors = False

def _checkForOpenBRCommandLineTool():
    # Get the Command-Line Tool path depending on your System.
    if open_br_executable != '':            # Override this Function
        return open_br_executable
    
    process = None
    if os.name == 'posix':                  # *nix based systems
        process = Popen(['which', 'br'], stdout=PIPE, stderr=PIPE)
    elif platform.system() == 'Windows':    # Windows
        process = Popen(['where', 'br'], stdout=PIPE, stderr=PIPE)
    else:
        raise Exception("System not supported.")

    stdout, stderr = process.communicate()
    stderr = stderr.decode("utf-8").replace("\n","")
    if print_errors:
        if stderr != '': print(stderr)
    
    return stdout.decode("utf-8").replace("\n","")

def _getTempPath():
    # Get a Temporary Path in /tmp or %TEMP% (System-dependent)
    basePath = "/tmp/"
    if platform.system() == "Windows":
        basePath = Popen(['ECHO', '%Temp%'], stdout=PIPE).communicate().decode("utf-8").replace("\n","")
    
    rdfile = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(15))
    while(os.path.isfile(os.path.join(basePath, rdfile))):
        rdfile = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(15))
   
    return os.path.join(basePath, rdfile)

def _prioritize_args(args, outputPath):
    # Re-arrange some arguments. (Sometimes Segmentation Faults are caused, if this isn't done)
    priorityList = ('-gui', '-algorithm')
    
    p_args = []
    r_args = []
    for a in args:
        if a.startswith(priorityList):
            indx = priorityList.index(a.split(" ")[0])
            p_args.insert(indx, a)
        else:
            r_args.append(a)

    return p_args + r_args + [outputPath]