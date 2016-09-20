import arrow
import geojson
from voluptuous import Any, Schema

from skywiserestclient import SkyWiseJSON
from skywiserestclient.validation import (datetime, polygon, multipolygon, datetime_to_str)
from skywiserestclient import SkyWiseException

from . import PlatformResource
from .style import Style
from .frame import ProductFrame
from .tile import GoogleMapsTile, BingMapsTile
from .datapoint import Datapoint
from .forecast import Forecast


class ProductException(SkyWiseException):
    pass


class Product(SkyWiseJSON, PlatformResource):
    """
    The Product class allows you to query platform products. More importantly,
    Product instances provide convenience methods for accessing other resources on
    Platform: frames, styles, datapoints, and map tiles.
    """

    _path = '/products'

    _deserialize = Schema({
        "id": unicode,
        "name": unicode,
        "description": unicode,
        "contentType": unicode,
        "source": unicode,
        "frames": Any(None, unicode),
        "forecasts": Any(None, unicode),
        "styles": unicode,
        "styleableLayers": [{
            "name": unicode,
            "type": unicode,
            "unit": Any(None, dict),
            "attributes": [dict]
        }],
        "coverage": {
            "geometry": Any(polygon, multipolygon),
            "type": unicode
        },
        "startTime": datetime,
        "endTime": datetime,
        "aggregationPeriodInMinutes": int
    })

    _serialize = Schema({
        "id": unicode,
        "name": unicode,
        "description": unicode,
        "contentType": unicode,
        "source": unicode,
        "frames": Any(None, unicode),
        "forecasts": Any(None, unicode),
        "styles": unicode,
        "styleableLayers": [{
            "name": unicode,
            "type": unicode,
            "unit": Any(None, dict),
            "attributes": [dict]
        }],
        "coverage": {
            "geometry": geojson.dumps,
            "type": unicode
        },
        "startTime": datetime_to_str,
        "endTime": datetime_to_str,
        "aggregationPeriodInMinutes": int
    })

    _args = Schema({
        "contentType": str,
        "source": str,
        "aggregation": int,
        "start": datetime_to_str,
        "end": datetime_to_str,
        "coverage": geojson.dumps
    })

    def __repr__(self):
        try:
            return '<Product %s>' % (self.name,)
        except:
            return super(Product, self).__repr__()

    @classmethod
    def find(cls, id_=None, aggregation=None, **kwargs):
        if aggregation is None:
            return super(Product, cls).find(id_=id_, **kwargs)

        if aggregation == 'day':
            aggregation = 1440
        elif aggregation == 'hour':
            aggregation = 60
        elif aggregation == 'minute':
            aggregation = 1

        return super(Product, cls).find(id_=id_, aggregation=aggregation, **kwargs)

    def aggregation(self):
        minutes = self.aggregationPeriodInMinutes
        if minutes == 1440:
            return 'day'
        elif minutes == 60:
            return 'hour'
        elif minutes == 1:
            return 'minute'

    def get_styles(self, **kwargs):
        """
        Requests all styles associated with the product.

        Returns:
           list of Style

        """
        return Style.find(self.id)

    def get_forecasts(self, **kwargs):
        return Forecast.find(product_id=self.id, **kwargs)

    def get_frames(self, start=None, end=None, limit=None, reruns=None, **kwargs):
        """Requests all frames for the product.

        Args:
            start (datetime): The start date for your frame date range.
            end (datetime): The end date for your frame date range.
            limit (int): The maximum number of frames you are requesting.
            reruns (bool): Whether or not you would like multiple frames for particular time.

        Returns:
            list of ProductFrame
            list of ForecastFrame
        """
        if self.frames:
            return ProductFrame.find(self.id, start=start, end=end, limit=limit, reruns=reruns, **kwargs)
        else:
            return self._get_forecast_frames(self.aggregation(), start=start, end=end)

    def _get_forecast_frames(self, interval, start=None, end=None):
        """ Get all frames for a product's forecasts in a given range, prioritizing the most current. """
        if start is None or end is None:
            forecast = Forecast.current(self.id)
            return forecast.get_frames(start=start, end=end)

        forecasts = Forecast.find(product_id=self.id)
        forecasts.sort(key=lambda f: f.initTime)
        forecasts.reverse()

        valid_times = arrow.Arrow.range(interval, arrow.get(start), arrow.get(end))
        frames = []
        for forecast in forecasts:
            if not valid_times:
                break
            frame_slice = forecast.get_frames(start=start, end=end)
            while frame_slice and valid_times:
                frame = frame_slice.pop()
                valid_times_covered = []
                valid_times_not_covered = []
                while valid_times:
                    valid_time = valid_times.pop()
                    if valid_time == frame.validTime:
                        frame.product = self
                        frames.append(frame)
                        valid_times_covered.append(valid_time)
                    else:
                        valid_times_not_covered.append(valid_time)
                valid_times = valid_times_not_covered

        return frames

    def bing_maps_tiles(self, quadkey, media_type=None, **kwargs):
        """Request Bing map tiles for the product.
        """
        if media_type:
            BingMapsTile.set_media_type(media_type)
        frames = self.get_frames(**kwargs)
        tile_requests = []
        for frame in frames:
            tr = BingMapsTile.find_async(frame.id, quadkey)
            tr.tag(frame=frame, product=self)
            tile_requests.append(tr)
        tiles = self.map(tile_requests)
        return tiles

    def google_maps_tiles(self, x, y, z, media_type=None, **kwargs):
        tile_requests = self.google_maps_tiles_async(x, y, z, media_type=media_type, **kwargs)
        return self.map(tile_requests)

    def google_maps_tiles_async(self, x, y, z, media_type=None, **kwargs):
        if media_type:
            GoogleMapsTile.set_media_type(media_type)
        frames = self.get_frames(**kwargs)
        tile_requests = []
        for frame in frames:
            tr = GoogleMapsTile.find_async(frame.id, x, y, z)
            tr.tag(frame=frame, product=self)
            tile_requests.append(tr)
        return tile_requests

    def google_maps_tileset(self, bounding_box, padding=None, zoom=None, media_type=None, **kwargs):
        requests = self.google_maps_tileset_async(bounding_box, padding=padding, zoom=zoom, media_type=media_type, **kwargs)
        return self.map(requests)

    def google_maps_tileset_async(self, bounding_box, padding=None, zoom=None, media_type=None, **kwargs):
        if media_type:
            GoogleMapsTile.set_media_type(media_type)
        frames = self.get_frames(**kwargs)

        requests = []
        for frame in frames:
            frame_zoom = zoom or frame.zoomLevels['native']
            tileset = GoogleMapsTile.tileset_async(frame.id, bounding_box, frame_zoom, padding)
            for tile in tileset:
                tile.tag(frame=frame, product=self)
            requests.extend(tileset)

        return requests

    def get_datapoints(self, latitude, longitude, **kwargs):
        reqs = self.get_datapoints_async(latitude, longitude, **kwargs)
        return self.map(reqs, raise_on_error=True)

    def get_datapoints_async(self, latitude, longitude, **kwargs):
        dp_requests = []
        for frame in self.get_frames(**kwargs):
            dpr = Datapoint.find_async(frame, latitude, longitude, **kwargs)
            dpr.tag(frame=frame, product=self)
            dp_requests.append(dpr)
        return dp_requests
