import os

from skywiserestclient import SkyWiseResource


class PlatformResource(SkyWiseResource):
    pass

_site = os.getenv('SKYWISE_PLATFORM_SITE', 'http://platform.api.wdtinc.com')
_user = os.getenv('SKYWISE_PLATFORM_APP_ID', '')
_password = os.getenv('SKYWISE_PLATFORM_APP_KEY', '')

PlatformResource.set_site(_site)
PlatformResource.set_user(_user)
PlatformResource.set_password(_password)

from .frame import ProductFrame, ForecastFrame
from .product import Product
from .forecast import Forecast
from .tile import BingMapsTile, GoogleMapsTile
from .datapoint import Datapoint
from .style import Style
from skywiserestclient import map_requests
