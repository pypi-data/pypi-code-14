# coding: utf-8

import os.path
import pytest
import cnregion
from pytest import mark
from cnregion import InvalidRegionException


@mark.parametrize('code,name,stack_name_str,level,has_subregions', [
    ('156110000000000', u'北京市', u'中国/北京市', 'province', True),
    ('156110107000000', u'石景山区', u'中国/北京市/市辖区/石景山区', 'county', True),
    ('156130131042843', u'杨家桥乡', u'中国/河北省/石家庄市/平山县/杨家桥乡', 'township', False),
    ('156000000000000', u'中国', u'中国', 'country', True),
])
def test_get_region(code, name, stack_name_str, level, has_subregions):
    region = cnregion.get_region(code)
    assert region is not None
    assert region.code == code
    assert region.name == name
    assert '/'.join([r.name for r in region.stack]) == stack_name_str
    assert region.level == level
    assert has_subregions == bool(list(region.get_subregions()))


@mark.parametrize('code', [
    '123',
])
def test_get_region_failed(code):
    with pytest.raises(InvalidRegionException):
        cnregion.get_region(code)


@mark.parametrize('name,region_code', [
    (u'中国 辽宁省 沈阳市 和平区 城区', '156210102050829'),
    (u'中国 辽宁省 沈阳市 和平区', '156210102000000'),
    (u'中国 陕西 咸阳市 杨凌区', '156610403000000'),
])
def test_get_region_by_stack_name(name, region_code):
    region = cnregion.get_region_by_stack_name(name)
    assert region is not None
    assert region.code == region_code


@mark.parametrize('region_code1,region_code2', [
    (u'156210102050829', '156210102000000'),
    (u'156210102050829', '156210000000000'),
    (u'156210102050829', '156000000000000')
])
def test_region_is_in_other(region_code1, region_code2):
    region1 = cnregion.get_region(region_code1)
    region2 = cnregion.get_region(region_code2)
    assert region1.is_in_region(region2)


@mark.parametrize('region_code1,region_code2', [
    (u'156210102050829', '156130102000000'),
    (u'156210102050829', '156130000000000')
])
def test_region_is_not_in_other(region_code1, region_code2):
    region1 = cnregion.get_region(region_code1)
    region2 = cnregion.get_region(region_code2)
    assert not region1.is_in_region(region2)


@mark.parametrize('region_code1,region_codes', [
    (u'156210102050829', ['156210102000000', '156130102000000']),
])
def test_region_is_in_others(region_code1, region_codes):
    region1 = cnregion.get_region(region_code1)
    other_regions = [cnregion.get_region(code) for code in region_codes]
    assert region1.is_in_regions(other_regions)


@mark.parametrize('code,subregion_codes', [
    ('156110000000000', ['156110100000000', '156110200000000']),
    ('156110111051536', []),
])
def test_get_subregions(code, subregion_codes):
    region = cnregion.get_region(code)
    assert region is not None
    assert region.code == code
    assert sorted(subregion_codes) == sorted([r.code for r in region.get_subregions()])


@mark.parametrize('china_province_codes', [
    ['156110000000000', '156120000000000', '156130000000000', '156140000000000',
     '156150000000000', '156210000000000', '156220000000000', '156230000000000',
     '156310000000000', '156320000000000', '156330000000000', '156340000000000',
     '156350000000000', '156360000000000', '156370000000000', '156410000000000',
     '156420000000000', '156430000000000', '156440000000000', '156450000000000',
     '156460000000000', '156500000000000', '156510000000000', '156520000000000',
     '156530000000000', '156540000000000', '156610000000000', '156620000000000',
     '156630000000000', '156640000000000', '156650000000000', '156710000000000',
     '156810000000000', '156820000000000']])
def test_get_china_provinces(china_province_codes):
    china = cnregion.get_region('156000000000000')
    assert sorted(china_province_codes) == sorted([r.code for r in china.get_subregions()])


@mark.parametrize('top_region_codes', [
    ['156000000000000', '999000000000000']])
def test_top_regions(top_region_codes):
    assert sorted(top_region_codes) == sorted([r.code for r in cnregion.get_top_regions()])


@mark.parametrize('code,result', [
    ("156632723018278", [("29", u"青海"), ("2612", u"玉树州"), ("2614", u"称多县"), ("18278", u"称文镇")]),
    ("156110103000000", [("1", u"北京"), ("2803", u"崇文区"), None, None]),
])
def test_jd_4level_code(code, result):
    region = cnregion.get_region(code)
    assert region.jd_4level_code == result


def _test_jd_4level_code_map(r):
    for i in r.get_subregions():
        _test_jd_4level_code_map(i)

    if r.level == 'country':
        return

    l = r.jd_4level_code
    if r.level == 'township':
        code = [i for i in l if i][-1][0].rjust(6, '0')
        assert r.code[-6:] == code


def test_jd_4level_code_map():
    for i in cnregion.get_top_regions():
        _test_jd_4level_code_map(i)


def test_get_deprecated_region():
    with open(os.path.join(os.path.dirname(__file__), 'region_codes.txt')) as f:
        region_codes = f.read().splitlines()

    for code in region_codes:
        cnregion.get_region(code)
