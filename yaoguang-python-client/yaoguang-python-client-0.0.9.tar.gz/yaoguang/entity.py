

from .exc import NoSuchEntity

from thriftpy.rpc import make_client
from thriftpy import load

from pkg_resources import resource_filename
from pygments import highlight, lexers, formatters

import json

CONTACT=1
COMPANY=2
AD=3

class Entities(object):

    def __init__(self, address, port=9196):
        thrift = load(resource_filename(__name__, "static/yaoguang.thrift"), module_name="yaoguang_thrift")
        self._client = make_client(thrift.ThriftInterface, address, port)

    def bj_tags_ready(self):
        return self._client.isReady("hello")


    """
    由于批量接口在 entity 不存在的时候不会抛出异常，所以在客户端做检查
    """
    def get_company(self, id, fields=[]):
        asJson = self._client.get(COMPANY, fields, [id])
        company = json.loads(asJson).get(id)

        if company is None:
           raise NoSuchEntity(id)
        return company

    def get_ad(self, id, fields=[]):
        asJson = self._client.get(AD, fields, [id])
        ad = json.loads(asJson).get(id)

        if ad is None:
           raise NoSuchEntity(id)
        return ad

    def get_contact(self, id, fields=[]):
        asJson = self._client.get(CONTACT, fields , [id])
        contact = json.loads(asJson).get(id)
    
        if contact is None:
            raise NoSuchEntity(id)
        return contact


    def get_contact_by_id(self, id):
        asJson = self._client.getByContactId(id)
        contact = json.loads(asJson)
        if contact is None:
            raise NoSuchEntity(id)
        return contact


    def get_ads(self, ids, fields=[]):
        asJson = self._client.get(AD, fields, ids)
        return json.loads(asJson)

    def get_contacts(self, ids, fields=[]):
        asJson = self._client.get(CONTACT, fields , ids)
        return json.loads(asJson)


class Entity(dict):
    def __init__(self, dic):
        dict.__init__(self)
        self.update(dic)

    def __repr__(self):
        return Entity._pretty_json(self)

    def __str__(self):
        return json.dumps(self)

    def ls(self):
        return '\n'.join(self.keys())

    @classmethod
    def _pretty_json(cls, dic, color=True):
        formatted_json = json.dumps(dic, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
        if color:
            return highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
        return formatted_json
