from zip_by_address.address_by_coordinates.address_by_coordinates_localizations.israel. \
    address_by_coordinates_resolver_israel import AddressByCoordinatesResolverIsrael


class AddressByCoordinatesClsFactory:
    country_to_address_resolver = {
        'israel': AddressByCoordinatesResolverIsrael
    }

    def __init__(self, country):
        self._country = country

    def create(self):
        address_by_coordinates_cls = self.country_to_address_resolver.get(self._country)
        if address_by_coordinates_cls is None:
            raise KeyError('No mapping configured for country {}'.format(self._country))
        return address_by_coordinates_cls

    @classmethod
    def get_supported_countries(cls):
        return cls.country_to_address_resolver.keys()
