class Address(tuple):
    def __new__(cls, country='', state='', city='', street='', street_number='', entrance='', apt='', pob=''):
        return super().__new__(cls, map(str, (country, state, city, street, street_number, entrance, apt, pob)))

    def __init__(self, country='', state='', city='', street='', street_number='', entrance='', apt='', pob=''):
        super().__init__()
        country, state, city, street, street_number, entrance, apt, pob = map(str, (
            country, state, city, street, street_number, entrance, apt, pob
        ))
        self.country = country
        self.state = state
        self.city = city
        self.street = street
        self.street_number = street_number
        self.entrance = entrance
        self.apt = apt
        self.pob = pob
