from zip_by_address.address_by_coordinates.address_by_coordinates_resolver import AddressByCoordinatesResolver


class AddressByCoordinatesResolverIsrael(AddressByCoordinatesResolver):
    def __init__(self, language='he', latitude=-1, longitude=-1):
        super().__init__(language, latitude, longitude)
