from requests.exceptions import ConnectionError

from ahoyhoy.lb.iloadbalancer import ILoadBalancer
from ahoyhoy.lb.providers.iprovider import IProvider

from ..utils import Host


class FakeLoadBalancer(ILoadBalancer):
    def __init__(self, endpoints_lst):
        self._up = endpoints_lst

    def _choose_next(self):
        return self._up[0]

    def pick(self):
        return self._choose_next()

    def update(self):
        pass


class FakeLoadBalancer2EPs(FakeLoadBalancer):

    def __init__(self, endpoints_lst):
        super(FakeLoadBalancer2EPs, self).__init__(endpoints_lst)
        self._index = 0

    def _choose_next(self):
        e = self._up[self._index]
        if self._index == 0:
            self._index = 1
        else:
            self._index = 0
        return e


class FakeFailedService(object):

    def __init__(self):
        self.calls = 0
        self.status_code = 200

    def get(self, *args, **kwargs):
        if self.calls == 0:
            self.calls += 1
            raise ConnectionError
        return "Good response"


class fakeclient(object):
    def __init__(self, session=None):
        self.session = session

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class FakeResponse(object):

    def __init__(self):
        self.status_code = 200
        self.text = "Some response"


class FakeSession(object):

    def __init__(self):
        self.headers = {}

    def get(self, *args):
        return FakeResponse()


class FakeProvider(IProvider):

    def __init__(self):
        self._calls = 0

    def get_list(self):
        if self._calls == 0:
            # return all bad hosts first
            self._calls += 1
            return Host('badhost2.bla', 80), Host('google1.com1', 80), Host('badhost3.bla', 80)
        else:
            # return some good hosts
            return Host('badhost2.bla', 80), Host('google.com', 80), Host('badhost3.bla', 80)
