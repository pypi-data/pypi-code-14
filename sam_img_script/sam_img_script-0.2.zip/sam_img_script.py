from PIL import Image
import os, shutil,argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d","--details",help = "Include this to display information about matched images", action = "store_true")
args = parser.parse_args()

active_path = os.getcwd()  #Gives path from where script is run
count = 0                  #Counts No. of images that match the criteria
target_dir_path = active_path + '/Matched_Image'    #Matched Images are kept in this folder
if os.path.isdir(target_dir_path) == False:			#If there is no such directory
 os.makedirs(target_dir_path)						#Create directory with that name

for root, dirs, files in os.walk(active_path, topdown=False):
 for name in files:
  try:
   path = os.path.join(root, name)
   im = Image.open(path)
   width,height=im.size
   if width<1024 and height<768:
    if args.details: 
     print(name,'  ', path , im.format,"%dx%d" % im.size)
    if shutil.copy2(path,target_dir_path):
     count = count + 1
  except IOError:
   pass
print("\n %d  Images copied to Matched_Image folder" %count)
input_key = input("Press any key")