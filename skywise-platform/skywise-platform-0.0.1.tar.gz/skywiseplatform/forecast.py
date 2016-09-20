from voluptuous import Any, Schema

from skywiserestclient import SkyWiseJSON

from skywiserestclient.validation import datetime, datetime_to_str
from skywiserestclient.exceptions import MissingParametersException
from skywiserestclient.skywise import SkyWiseException
from skywiseplatform import PlatformResource, ForecastFrame


_forecast_deserialize_schema = Schema({
    "id": unicode,
    "initTime": datetime,
    "frames": unicode,
    "product": unicode
})

_forecast_serialize_schema = Schema({
    "id": unicode,
    "initTime": datetime_to_str,
    "frames": unicode,
    "product": unicode
})


class Forecast(SkyWiseJSON, PlatformResource):

    _path = '/forecasts'

    _deserialize = _forecast_deserialize_schema
    _serialize = _forecast_serialize_schema

    @classmethod
    def find(cls, id_=None, product_id=None, **kwargs):
        if id_:
            return super(Forecast, cls).find(id_)
        elif product_id:
            return _ProductForecast.find(product_id, **kwargs)
        raise MissingParametersException("Must specify either forecast id or product.")

    @classmethod
    def current(cls, product_id):
        """ Returns most recent forecast for specified product. """
        return _ProductForecast.current(product_id)

    def __repr__(self):
        try:
            return '<Forecast %s>' % (self.initTime,)
        except:
            return super(Forecast, self).__repr__()


class _ProductForecast(SkyWiseJSON, PlatformResource):

    _path = "/products/{product_id}/forecasts"

    _deserialize = _forecast_deserialize_schema
    _serialize = _forecast_serialize_schema

    _args = Schema({
        "start": datetime_to_str,
        "end": datetime_to_str,
        "limit": int,
        "sort": Any("asc", "desc")
    })

    @classmethod
    def find(cls, product_id, **kwargs):
        forecasts = super(_ProductForecast, cls).find(product_id=product_id, **kwargs)
        if len(forecasts) == 0:
            raise SkyWiseException("No forecasts found for product.")
        return forecasts

    @classmethod
    def current(cls, product_id):
        forecasts = cls.find(product_id)
        forecasts.sort(key=lambda f: f.initTime)
        return forecasts[-1]

    def get_frames(self, start=None, end=None, **kwargs):
        return ForecastFrame.find(self.id, start=start, end=end, **kwargs)

    def __repr__(self):
        try:
            return '<Forecast %s>' % (self.initTime,)
        except:
            return super(Forecast, self).__repr__()
