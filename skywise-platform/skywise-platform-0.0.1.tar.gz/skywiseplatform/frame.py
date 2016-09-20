"""
Created on 01/27/2016
@author: Justin Stewart
"""
from voluptuous import Any, Schema

from skywiserestclient import SkyWiseJSON
from skywiserestclient.validation import datetime, datetime_to_str

from . import PlatformResource


class _Frame(SkyWiseJSON, PlatformResource):

    _args = Schema({
        "start": datetime_to_str,
        "end": datetime_to_str,
        "limit": int,
        "sort": Any("asc", "desc"),
        "reruns": bool
    })

    _deserialize = Schema({
        "id": unicode,
        "validTime": datetime,
        "runTime": datetime,
        "creationTime": datetime,
        "zoomLevels": {
            "minimum": int,
            "native": int,
            "maximum": int
        },
        "mediaTypes": [Any("image/jpeg", "image/png", "image/tiff")],
        "tileSize": int,
        "forecast": Any(None, unicode),
        "product": unicode
    })

    _serialize = Schema({
        "id": unicode,
        "validTime": datetime_to_str,
        "runTime": datetime_to_str,
        "creationTime": datetime_to_str,
        "zoomLevels": {
            "minimum": int,
            "native": int,
            "maximum": int
        },
        "mediaTypes": [Any("image/jpeg", "image/png", "image/tiff")],
        "tileSize": int,
        "forecast": Any(None, unicode),
        "product": unicode
    })


class SingleFrame(_Frame):

    _path = "/frames"


class ProductFrame(_Frame):
    """Requests product frames.
    """

    _path = "/products/{product_id}/frames"

    @classmethod
    def find(cls, product_id, start=None, end=None, limit=None, sort=None, reruns=None, **kwargs):
        """Requests frames for a product.

        Example:
            .. code-block:: python

               import skywise

        Args:
            product_id (str): the product you're requesting frames for.
            start (datetime): The start date for your frame date range.
            end (datetime): The end date for your frame date range.
            limit (int): The maximum number of frames you are requesting.
            reruns (bool): Whether or not you would like multiple frames for particular time.

        Returns:
            list of ProductFrame: A list of frames for the product.

        """
        return super(ProductFrame, cls).find(product_id=product_id, start=start, end=end,
                                             limit=limit, sort=sort, reruns=reruns, **kwargs)


class ForecastFrame(_Frame):
    """Requests Forecast Frames.

    Attributes:
        id (str): the frame's id.
        validTime (datetime): when the frame is valid
        runTime (datetime): when the frame was ran
        zoomLevels (dict): minimum, native, and maximum zoom level specifications
        mediaTypes (str): list of supported types: image/jpeg, image/png, or image/tiff
        tileSize (int): tile size
        forecast (str): url to the frame's forecast
    """
    _path = "/forecasts/{forecast_id}/frames"

    @classmethod
    def find(cls, forecast_id, start=None, end=None, limit=None, sort=None, reruns=None, **kwargs):
        """Requests frames for a product.

        Example:
            .. code-block:: python

                forecast_id = Product.find('weatherops-24hr-precipitation-forecast').id

                # Retrieve latest frames
                frames = ForecastFrame.find(product_id) 

                # Retrieve frames for next few days
                start = arrow.get().datetime
                end = arrow.get().replace(days=+5).datetime
                frames = ForecastFrame.find(forecast_id, start=start, end=end, limit=3, sort="desc")

        Args:
            forecast_id (str): the forecast you're requesting frames for.
            start (datetime): The start date for your frame date range.
            end (datetime): The end date for your frame date range.
            limit (int): The maximum number of frames you are requesting.
            reruns (bool): Whether or not you would like multiple frames for particular time.

        Returns:
            list of ForecastFrame: A list of frames for the product.

        """
        return super(ForecastFrame, cls).find(forecast_id=forecast_id, start=start, end=end,
                                              limit=limit, sort=sort, reruns=reruns, **kwargs)
