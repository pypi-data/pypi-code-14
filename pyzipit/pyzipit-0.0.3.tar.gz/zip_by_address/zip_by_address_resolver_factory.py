from zip_by_address.zip_by_address_localizations.israel.zip_by_address_israel import ZipByAddressIsrael


class ZipResolverClsFactory:
    country_to_zip_resolver = {
        'israel': ZipByAddressIsrael
    }

    def __init__(self, country):
        self._country = country

    def create(self):
        zip_by_address_cls = self.country_to_zip_resolver.get(self._country)
        if zip_by_address_cls is None:
            raise KeyError('No mapping configured for country {}'.format(self._country))
        return zip_by_address_cls

    @classmethod
    def get_supported_countries(cls):
        return cls.country_to_zip_resolver.keys()
