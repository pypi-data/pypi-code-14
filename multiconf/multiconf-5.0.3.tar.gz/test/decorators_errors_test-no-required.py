# Copyright (c) 2012 Lars Hupfeldt Nielsen, Hupfeldt IT
# All rights reserved. This work is under a BSD license, see LICENSE.TXT.

from __future__ import print_function

# pylint: disable=E0611
from pytest import raises
from .utils.utils import config_error, config_warning, lineno, total_msg, assert_lines_in, mc_required_current_env_expected

from .. import ConfigRoot, ConfigItem, ConfigException, MC_REQUIRED
from ..decorators import named_as, nested_repeatables, ConfigDefinitionException
from ..envs import EnvFactory

ef1_prod = EnvFactory()
prod1 = ef1_prod.Env('prod')

ef2_prod_dev2ct = EnvFactory()
dev2ct = ef2_prod_dev2ct.Env('dev2ct')
prod2 = ef2_prod_dev2ct.Env('prod')


def ce(line_num, *lines):
    return config_error(__file__, line_num, *lines)

def cw(line_num, *lines):
    return config_warning(__file__, line_num, *lines)


def test_decorator_arg_not_a_valid_identifier_in_nested_repeatables_decorator():
    with raises(ConfigDefinitionException) as exinfo:
        @nested_repeatables('a, a-b, b, 99')
        class root(ConfigRoot):
            pass

    assert str(exinfo.value) == "['a-b', '99'] are not valid identifiers"


def test_decorator_arg_is_keyword_in_nested_repeatables_decorator():
    with raises(ConfigDefinitionException) as exinfo:
        @nested_repeatables('a, b, def, c')
        class root(ConfigRoot):
            pass

    assert str(exinfo.value) == "'def' is not a valid identifier"


def test_required_attributes_inherited_missing(capsys):
    class root(ConfigRoot):
        def __init__(self, selected_env, ef):
            super(root, self).__init__(selected_env, ef)
            self.anattr = MC_REQUIRED
            self.anotherattr = MC_REQUIRED

    class root2(root):
        def __init__(self, selected_env, ef):
            super(root2, self).__init__(selected_env, ef)
            self.someattr2  = MC_REQUIRED
            self.someotherattr2 = MC_REQUIRED

    with raises(ConfigException) as exinfo:
        with root2(prod1, ef1_prod) as cr:
            cr.setattr('anattr', prod=1)
            cr.setattr('someattr2', prod=3)
            cr.setattr('someotherattr2', prod=4)
            errorline = lineno()

    _sout, serr = capsys.readouterr()
    assert serr == ce(errorline, mc_required_current_env_expected.format(attr='anotherattr'))


def test_decorator_arg_not_a_valid_identifier_in_named_as_decorator():
    with raises(ConfigDefinitionException) as exinfo:
        @named_as('a-b')
        class root(ConfigRoot):
            pass

    assert str(exinfo.value) == "'a-b' is not a valid identifier"


def test_decorator_arg_is_a_keyword_in_named_as_decorator():
    with raises(ConfigDefinitionException) as exinfo:
        @named_as('class')
        class root(ConfigRoot):
            pass

    assert str(exinfo.value) == "'class' is not a valid identifier"
    
