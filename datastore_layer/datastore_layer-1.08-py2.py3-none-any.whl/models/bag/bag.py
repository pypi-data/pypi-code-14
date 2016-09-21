from datastore_layer.models.dated_model_base import DatedModelBase
from datastore_layer.models.property_types import create_property, PropertyTypes


class Bag(DatedModelBase):
    mac_id = create_property(PropertyTypes.String, required=True)
    serial_number = create_property(PropertyTypes.String, required=True)
    bag_type = create_property(PropertyTypes.Integer, required=True)
    passcode = create_property(PropertyTypes.String)
    name = create_property(PropertyTypes.String)
    owner_key = create_property(PropertyTypes.Key, kind="User")
