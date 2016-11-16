#!/usr/bin/py
from PIL import Image                                    #imports "Image" class of PIL library
import os, shutil, argparse                                       #Imports the OS library

parser = argparse.ArgumentParser()

parser.add_argument("--verbosity", help = "sam sam sam")
args = parser.parse_args()
for root, dirs, files in os.walk(".", topdown=False):    #os-walk scans all the directories from bottom to up and the current directory is the directory which currently holds the file.
 for name in files:                                      #starts the loop
  try:                                                   #exception handling code
   path = os.path.join(root, name)                       #concatenates the root and name of the file and store it in path
   im = Image.open(path)                                 #Passes the file in "Open" method of image class and stores the file in im variable
   width,height=im.size                                  #im.size returns the size of the file. Eg. if  the image size is 100*600 it stores width = 100 and height = 600
   if width<1024 and height<768:
      if args.verbosity:                                   #if condition to match the criteria of the task
         print(name,'  ', path , im.format,"%dx%d" % im.size) #if the criteria matches, the program prints the name, path, format and size of the file
         shutil.copy2(path,'../Matched/')                     #the files with the matching criteia are then copied to a file named 'Matched' in the parent directory
  except IOError:                                        #exception handling code
   pass                                                  #return 0