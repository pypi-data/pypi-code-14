#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Copyright 2016 Daniel Ross Creager

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

#------------------------------------------------------------------------------#
# Script:   Deploy.py
# Written:  November 2016
# Author:   Daniel R Creager
# Desc:     Management an AWS CodeDeploy Package 
#------------------------------------------------------------------------------#
'''
import os, sys
from com.danielcreager.Profile    import Profile
from com.danielcreager.CodeDeploy import ToolBox

def main():
    #------------------------------------------------------------------------------#
    # Validate Input arguments
    #------------------------------------------------------------------------------#
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: deploy <profile.ini>\n")
        sys.exit(-1)

    if not os.path.exists(sys.argv[1]):
        sys.stderr.write("ERROR: Profile '%s' was not found!\n" % (sys.argv[1]))
        sys.exit(-1)

    #------------------------------------------------------------------------------#
    # Instantiate: a AWSToolBox object
    # - CodeDeploy Profile 
    # - CodeDeploy Toolbox
    #------------------------------------------------------------------------------#
    tb = ToolBox(Profile(sys.argv[1:]))
    
    #------------------------------------------------------------------------------#
    # Print a Job header
    # Make a deployment package
    #------------------------------------------------------------------------------#
    tb.printHeader()
    s3Obj = tb.makePkg()
    
    #------------------------------------------------------------------------------#
    # OnS3ObjectPresent: Execute the deployment package
    #------------------------------------------------------------------------------#
    if s3Obj != None: 
        tb.runPkg()

if __name__ == "__main__":
    main()