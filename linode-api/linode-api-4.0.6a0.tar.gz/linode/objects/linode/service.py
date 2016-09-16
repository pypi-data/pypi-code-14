from .. import Base, Property

class Service(Base):
    api_name = 'services'
    api_endpoint = "/linode/services/{id}" #TODO - this 404's
    properties = {
        'storage': Property(filterable=True),
        'hourly_price': Property(filterable=True),
        'backups_price': Property(filterable=True),
        'id': Property(identifier=True),
        'label': Property(filterable=True),
        'mbits_out': Property(filterable=True),
        'monthly_price': Property(filterable=True),
        'ram': Property(filterable=True),
        'transfer': Property(filterable=True),
        'vcpus': Property(filterable=True),
    }
