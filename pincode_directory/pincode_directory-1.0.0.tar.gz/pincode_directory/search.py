import string
from pincodes import pincodes

def search_with_pincode(pincode):
    '''Searching the location with using the pincode. It's expect the 6 digit number.'''
    if isinstance(pincode,int) or isinstance(pincode,str):
        pincode = str(pincode)
    else:
        raise ValueError('Invalid input')
    if len(pincode) == 6:
        try:
            location_deatils = pincodes[pincode]
            return location_deatils
        except KeyError:
            raise ValueError('Pincode Not exist in the directory')
    else:
        raise Exception('Not a valid pincode')

def search_with_location(location):
    '''Searching the pincode with using the location. It's expect the valid location.'''
    if not isinstance(location,str):
        raise ValueError('Invalid input')
    pincode = None
    for key,val in pincodes.iteritems():
        if location.lower() in ' '.join(val).lower():
            pincode = key
            break
    if pincode:
        return pincode
    else:
        raise ValueError('Location not in the Pincode directory')
