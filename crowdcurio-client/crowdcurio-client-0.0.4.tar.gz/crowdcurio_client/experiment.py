import datetime
import requests
import time

from crowdcurio_client.crowdcurio import (
    CrowdCurioAPIException, CrowdCurioObject
)

class Experiment(CrowdCurioObject):
    _api_slug = 'experiment'
    _link_slug = 'experiment'
    _edit_attributes = (
        'name',
        'status',
        'params',
        'restrictions',
    )

    @classmethod
    def find(cls, id='', slug=None):
        if not id and not slug:
            return None
        return cls.where(id=id, slug=slug).next()

    def add(self, project, curio, task):
        self.put(
            '{}'.format(self.id),
            json={"data": {"type": "Experiment", "id": self.id, "relationships": {"project":{ "data": { "type": "Project", "id": project.id}}, "curio":{ "data": {"type": "Curio", "id": curio.id}}, "task":{ "data": {"type": "Task", "id": task.id}} }}}
        )

    def remove(self, project, curio, task):
        self.put(
            '{}'.format(self.id),
            json={"data": {"type": "Experiment", "id": self.id, "relationships": {"project":{}, "curio":{}, "task":{} }}}
        )


class Condition(CrowdCurioObject):
    _api_slug = 'condition'
    _link_slug = 'condition'
    _edit_attributes = (
        'name',
        'configuration',
        'nb_subjects',
        'max_subjects',
        'status',
    )

    @classmethod
    def find(cls, id=''):
        if not id:
            return None
        return cls.where(id=id).next()

    def add(self, experiment):
        self.put(
            '{}'.format(self.id),
            json={"data": {"type": "Condition", "id": self.id, "relationships": {"experiment":{"data":{"type":"Experiment","id":experiment.id}}}}}
        )

    def remove(self, experiment):
        self.put(
            '{}'.format(self.id),
            json={"data": {"type": "Condition", "id": self.id, "relationships": {"experiment":{}}}}
        )

    def delete(self):
        self.delete('{}'.format(self.id)
        )