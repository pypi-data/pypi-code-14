import datetime
import requests
import time

from crowdcurio_client.crowdcurio import (
    CrowdCurioAPIException, CrowdCurioObject
)

class DataSet(CrowdCurioObject):
    _api_slug = 'dataset'
    _link_slug = 'dataset'
    _edit_attributes = (
        'name',
        'is_active',
    )

    @classmethod
    def find(cls, id='', slug=None):
        if not id and not slug:
            return None
        return cls.where(id=id, slug=slug).next()

    def add(self, curio):
        self.put(
            '{}'.format(self.id),
            json={"data": {"type": "Dataset", "id": self.id, "relationships": {"curio":{"data":{"type":"Curio","id":curio.id}}}}}
        )

    def remove(self, curio):
        self.put(
            '{}'.format(self.id),
            json={"data": {"type": "Dataset", "id": self.id, "relationships": {"curio":{}}}}
        )