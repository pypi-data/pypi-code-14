import logging

from djmessenger import settings
from geopy.distance import vincenty
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderServiceError


logger = logging.getLogger(__name__)


def get_geocoder():
    return GoogleV3(settings.DJM_GOOGLE_API_KEY)


def calculate_distance_coordinates(coordinate1, coordinate2):
    """

    :param coordinate1: (latitude, longitude)
    :type coordinate1: tuple
    :param coordinate2: (latitude, longitude)
    :type coordinate2: tuple
    :return: the distance between the 2 coordinates in meters
    :rtype: float
    """
    return calculate_distance(coordinate1[0], coordinate1[1],
                              coordinate2[0], coordinate2[1])


def calculate_distance(latitude_1, longitude_1, latitude_2, longitude_2):
    """
    Given 2 sets of coordinates, calculate the distance in kilometers and
    return an int and discard decimal points

    :param latitude_1: -90 to 90
    :type latitude_1: float

    :param longitude_1: -180 to 180
    :param latitude_2:
    :param longitude_2:

    :return: the distance between the 2 coordinates in meters
    :rtype: float

    :raise ValueError: if any of the coordinates is invalid
    """
    if -90 <= latitude_1 <= 90 \
            and -90 <= latitude_2 <= 90 \
            and -180 <= longitude_1 <= 180 \
            and -180 <= longitude_2 <= 180:
        return vincenty((latitude_1, longitude_1), (latitude_2, longitude_2)).meters
    else:
        raise ValueError('latitude ranges from -90 to 90 and longitude ranges '
                         'from -180 to 180, the data given was invalid')


def geocoding(location):
    """
    geocode a location

    :param location: a string
    :return: a tuple of (latitude, longitude)
    """
    coder = get_geocoder()
    res = None
    try:
        res = coder.geocode(location)
    except GeocoderServiceError as e:
        logger.error('geocoding failed with GeocoderServiceError because %s' %
                     str(e))
    if res:
        return res.latitude, res.longitude
    return None, None


# def reverse_geocoding(latitude, longitude):
#     """
#     Trying to find where this coordinates corresponding to, return a tuple of
#     (Country, Subdivision) if found
#
#     Note that if Country is not found, return None.
#     If country is found, subdivision is optional, so we return (Country, None)
#     if subdivision not found
#
#     :param longitude:
#     :type longitude: Decimal
#
#     :param latitude:
#     :type latitude: Decimal
#
#     :return: DefiningArea
#     :rtype: DefiningArea
#     """
#     from api.models import DefiningArea
#     coder = get_geocoder()
#     result = coder.reverse((latitude, longitude))
#     if not result:
#         return None
#     alpha2 = None
#     name = None
#     for location in reversed(result):
#         for component in location.raw['address_components']:
#             if 'country' in component['types']:
#                 if alpha2 is None:  # only set once
#                     alpha2 = component['short_name']
#             if 'administrative_area_level_1' in component['types']:
#                 if name is None:
#                     name = component['short_name']
#         if alpha2 is not None and name is not None:
#             break
#     area = None
#     # this is to find the defining area which is also a country because country
#     # unique_in_county is True
#     if alpha2:
#         try:
#             area = DefiningArea.search(alpha2)
#         except DefiningArea.DoesNotExist:
#             pass
#     if name:
#         try:
#             area = DefiningArea.search(name)
#         except DefiningArea.DoesNotExist:
#             pass
#     return area
