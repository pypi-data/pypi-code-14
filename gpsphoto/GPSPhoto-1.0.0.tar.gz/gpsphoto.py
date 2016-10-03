# GPSPhoto
# Programmer: Jess Williams
# EMail: stripes.denomino@gmail.com
# Purpose: extracts and converts GPS Data from Photos

# Import Modules
import math
import os
import sys
import ast
import exifread

''' Convert Degrees, Minutes and Seconds to decimal, passed in two
    parameters. 1 - a list consisting of degree, minute, and second or
    degree and minute. 2 - a reference of N S E W.  Assumption -
    all non decimal coordinate will have a reference'''
def coord2decimal(coord, quad):
    # Determine which type is being passed
    if len(coord) == 2:
        degree = coord[0]
        minute = coord[1]
        decimal = (minute/60) + degree
    elif len(coord) == 3:
        degree = coord[0]
        minute = coord[1]
        second = coord[2]
        decimal = (second/3600) + (minute/60) + degree

    # Determine Quadrant
    if quad == 'W' or quad == 'S':
        modifier = -1
    else:
        modifier = 1

    return decimal * modifier

''' Get All GPS Data from Image File, takes path to image file'''
def getGPSData(fileName):
    # Declare Local Variables
    # Get Raw GPS Data
    tags = getRawData(fileName)
    gpsDict = {}

    ''' There are 3 different types of Longitude and Latitude data stored.
        1, type is already in decimal format - Assumption no Ref Value
        2, type is in degree and minute format - Assumption [100, 44.5678]
        3, type is in degree, minute and second - Assumption [100, 44,95521/5000]
        This function will assume the assumptions are correct and parse the strings
        and return a list of floating elements, takes an parameter of list of
        strings'''        
    def parseItude(tude):
        #Declare Local Variables
        coordList = []

        # Determine which type
        if len(tude) == 3:
            coordList.append(float(tude[0].strip()))
            coordList.append(float(tude[1].strip()))
            if itude[2].find('/') > -1:
                seconds = tude[2].strip().split('/')
                val = float(seconds[0]) / float(seconds[1])
            else:
                val = float(tude[2].strip())
            coordList.append(val)
        elif len(itude) == 2:
            coordList.append(float(tude[0].strip()))
            coordList.append(float(tude[1].strip()))
        else:
            coordList.append(float(tude[0].strip()))
                
        return coordList
    
    for tag in tags.keys():
        if tag == 'GPS GPSTimeStamp':
            t = ast.literal_eval(str(tags[tag]))
            gpsDict['UTC-Time'] = str(t[0]) + ":" + str(t[1]) + ":" + str(t[2])
        elif tag == 'GPS GPSDate':
            d = str(tags[tag]).split(':')
            gpsDict['Date'] = str(d[1]) + "/" + str(d[2]) + "/" + str(d[0])
        elif tag == 'GPS GPSLatitude':
            itude = str(tags[tag]).strip('[').strip(']').split(',')
            var = parseItude(itude)
            if len(var) > 1:
                lat = coord2decimal(var, str(tags['GPS GPSLatitudeRef']))
            else:
                lat = float(var[0])
            gpsDict['Latitude'] = lat
        elif tag == 'GPS GPSLongitude':
            itude = str(tags[tag]).strip('[').strip(']').split(',')
            var = parseItude(itude)
            if len(var) > 1:
                lng = coord2decimal(var, str(tags['GPS GPSLongitudeRef']))
            else:
                lng = float(var[0])
            gpsDict['Longitude'] = lng
        elif tag == 'GPS GPSAltitude':
            altitude = int(str(tags[tag]))
            ref = int(str(tags['GPS GPSAltitudeRef']))
            if ref == 1:
                altitude = altitude * -1
            gpsDict['Altitude'] = altitude

    return gpsDict

''' Returns the raw GPS Data returned from ExifRead, takes
    string argument for the "/path/to/imagefile"'''
def getRawData(fileName):
    # Declare Local Variables
    gpsDict = {}
    
    # Open images file for reading (binary mode)
    image = open(fileName, 'rb')

    # Return Exif tags
    tags = exifread.process_file(image)
    
    # Get GPS Tags List
    tagKeys= []
    foundGPS = False
    for tag in tags.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):           
            # Search For GPS Data
            if tag.find('GPS') > -1:
                foundGPS = True
                tagKeys.append(tag)
                
    # Build Dictionary
    for tag in tagKeys:
        gpsDict[tag] = tags[tag]

    return gpsDict

''' Return Decimal Coordinates if used in command line
    Call command as follows:
    python gpsphoto.py "/path/to/1st/photo" "/path/to/2nd/photo"'''
if len(sys.argv) > 1:
    if sys.argv[1] == '-D':
        data = getRawData(sys.argv[2])
        for tag in data.keys():
            print "%s: %s" % (tag, data[tag])        
    else:
        data = getGPSData(sys.argv[1])
        for tag in data.keys():
            print "%s: %s" % (tag, data[tag])
