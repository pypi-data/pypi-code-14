import operator
import unittest
from functools import reduce

from adaptivepy.component.definitions import AdaptationSpace
from adaptivepy.component.proxyrouter import InternalProxyRouter,\
    ExternalProxyRouter, BaseProxyRouter, TargetNotACandidateException

from adaptivepy.monitor.parameter import DiscreteParameter

SOME_PARAM = "some_param"
OTHER_PARAM = "other_param"
YET_ANOTHER_PARAM = "yet_another_param"
arguments_provider = {
    SOME_PARAM: 4,
    OTHER_PARAM: 2
}


class SomeParameter(DiscreteParameter):
    s_state0 = 0
    s_state1 = 1
    s_state2 = 2


class OtherParameter(DiscreteParameter):
    o_state0 = 0
    o_state1 = 1


class CanDoSomething:
    def do_something(self):
        raise NotImplementedError()


@AdaptationSpace({SomeParameter: SomeParameter.get_range(0, 1)})
class Candidate1(CanDoSomething):
    def __init__(self, some_param, other_param):
        self.val = some_param + other_param

    def do_something(self):
        return self.val


@AdaptationSpace({SomeParameter: {SomeParameter.s_state2}})
class Candidate2(CanDoSomething):
    def __init__(self, sum_params):
        self.val = sum_params - 3

    def do_something(self):
        return self.val


@AdaptationSpace({OtherParameter: {OtherParameter.o_state1}})
class Candidate3(CanDoSomething):
    def __init__(self, some_param, other_param, yet_another_param):
        self.val = some_param * other_param - yet_another_param

    def do_something(self):
        return self.val


class TestBaseProxyRouter(BaseProxyRouter):
    @classmethod
    def candidates(cls, arguments_provider=None):
        some_param = arguments_provider.get(SOME_PARAM, 0)
        other_param = arguments_provider.get(OTHER_PARAM, 0)
        yet_another_param = arguments_provider.get(YET_ANOTHER_PARAM, 0)

        return {
            Candidate1: lambda: Candidate1(some_param, other_param),
            Candidate2: lambda: Candidate2(some_param + other_param),
            Candidate3: lambda: Candidate3(some_param,
                                           other_param,
                                           yet_another_param)
        }

    def __init__(self):
        super().__init__()
        self.candidate = Candidate1

    def arguments_provider(self):
        return arguments_provider

    def choose_route(self):
        return self.candidate


class TestInternalProxyRouter(TestBaseProxyRouter, InternalProxyRouter):
    pass


class TestExternalProxyRouter(TestBaseProxyRouter, ExternalProxyRouter):
    pass


def product(iterable):
    return reduce(operator.mul, iterable, 1)


class ProxyRouterTestCase(unittest.TestCase):

    def setUp(self):
        self.i_pxrt = TestInternalProxyRouter()
        self.e_pxrt = TestExternalProxyRouter()
        self.proxyrouters = (self.i_pxrt, self.e_pxrt)

    def test_route(self):
        def assertDoSomethingCallable(obj):
            self.assertTrue(callable(getattr(
                obj, CanDoSomething.do_something.__name__, None)))

        for pr in self.proxyrouters:
            self.assertIsNotNone(pr.proxy())
            proxy = pr.proxy()

            with self.assertRaises(TargetNotACandidateException):
                pr.route(None)

            pr.route(Candidate1)
            assertDoSomethingCallable(proxy)
            self.assertEqual(proxy.do_something(),
                             sum(list(arguments_provider.values())))

            pr.route(Candidate2)
            assertDoSomethingCallable(proxy)
            self.assertEqual(proxy.do_something(),
                             sum(list(arguments_provider.values())) - 3)

            pr.route(Candidate3)
            assertDoSomethingCallable(proxy)
            self.assertEqual(proxy.do_something(),
                             product(list(arguments_provider.values())))

if __name__ == '__main__':
    unittest.main()
