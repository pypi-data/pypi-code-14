# Copyright (c) 2012 Lars Hupfeldt Nielsen, Hupfeldt IT
# All rights reserved. This work is under a BSD license, see LICENSE.TXT.

from collections import OrderedDict

from .. import ConfigRoot, ConfigItem, RepeatableConfigItem, ConfigBuilder
from ..decorators import nested_repeatables, named_as, required
from ..envs import EnvFactory

from .utils.check_containment import check_containment


ef1_prod = EnvFactory()
prod1 = ef1_prod.Env('prod')

ef2_prod_pp = EnvFactory()
pp2 = ef2_prod_pp.Env('pp')
prod2 = ef2_prod_pp.Env('prod')


@named_as('xses')
@nested_repeatables('x_children')
class Xses(RepeatableConfigItem):
    def __init__(self, name):
        super(Xses, self).__init__(mc_key=name)
        self.name = name


@named_as('x_children')
class XChild(RepeatableConfigItem):
    def __init__(self, name):
        super(XChild, self).__init__(mc_key=name)
        self.name = name


class XBuilder(ConfigBuilder):
    def __init__(self, num):
        super(XBuilder, self).__init__()
        self.number = num

    def build(self):
        for num in range(1, self.number+1):
            Xses(name='server%d' % num)


@nested_repeatables('xses')
class Root(ConfigRoot):
    pass
        

def test_configbuilder_override_with_required_item():
    class b(ConfigItem):
        xx = 1

    with Root(prod2, ef2_prod_pp) as cr:
        with XBuilder(2) as xb:
            b()

    check_containment(cr, verbose=True)


def test_configbuilder_nested_items_access_to_contained_in():
    with Root(prod2, ef2_prod_pp) as cr:
        with XBuilder(2) as xb:
            with XChild(name='a') as x1:
                ci = ConfigItem()

    assert ci.contained_in == x1
    check_containment(cr, verbose=True)
    assert x1.contained_in != cr
