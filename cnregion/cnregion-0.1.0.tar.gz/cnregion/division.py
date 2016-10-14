# coding: utf-8

import simplejson
from pkg_resources import resource_string
from ._compat import unicode_type
from .utils import bisect_search_right


__all__ = ['Division']


class DivisionLevel(object):
    country = 'country'
    province = 'province'
    prefecture = 'prefecture'
    county = 'county'
    township = 'township'


class Division(object):
    _division_tree = []
    _jd_division_mappings = {}
    _jd_division = {}
    version = ''

    @classmethod
    def _traverse(cls, code, l):
        index = bisect_search_right(l, code, key=lambda x: x[0])
        if index == 0:
            return None

        return l[index-1]

    @classmethod
    def get_name(cls, code):
        current_divisions = cls._division_tree

        while current_divisions:
            record = cls._traverse(code, current_divisions)
            if not record:
                return None

            division_code, division_name_list, current_divisions = record
            if division_code == code:
                return division_name_list[0]

    @classmethod
    def get_stack(cls, code):
        code = unicode_type(code)
        current_divisions = cls._division_tree
        stack = []

        while current_divisions:
            record = cls._traverse(code, current_divisions)
            if not record:
                return stack

            division_code, division_name_list, current_divisions = record
            stack.append((division_code, division_name_list[0]))
        return stack

    @classmethod
    def traverse(cls, code):
        code = unicode_type(code)
        current_divisions = cls._division_tree

        while current_divisions:
            record = cls._traverse(code, current_divisions)
            if not record:
                return []

            division_code, division_name_list, current_divisions = record
            if division_code == code:
                return [(d_code, d_name_list[0]) for d_code, d_name_list, _ in current_divisions]
        return []

    @classmethod
    def is_subdivision_of(cls, code1, code2):
        code1, code2 = unicode_type(code1), unicode_type(code2)
        return code1 in [key for key, _ in cls.traverse(code2)]

    @classmethod
    def top_divisions(cls):
        return [(code, name_list[0]) for code, name_list, _ in cls._division_tree]

    @classmethod
    def get_level(cls, code):
        code = unicode_type(code)
        if code.endswith(u'000000000000'):
            return DivisionLevel.country
        elif code.endswith(u'0000000000'):
            return DivisionLevel.province
        elif code.endswith(u'00000000'):
            return DivisionLevel.prefecture
        elif code.endswith(u'000000'):
            return DivisionLevel.county
        else:
            return DivisionLevel.township

    @classmethod
    def jd_4level_code(cls, code):
        l = cls._jd_division_mappings.get(code)
        result = []
        for i in l:
            v = (i, cls._jd_division[i]) if int(i) else None
            result.append(v)
        return result

    @classmethod
    def is_placeholder(cls, code):
        '''省直辖县级行政区划/自治区直辖县级行政区划。不属于正常地区，占位连接直辖县'''
        if code in ('156419000000000', '156429000000000',
                    '156469000000000', '156659000000000'):
            return True
        return False

    @classmethod
    def get_code_by_name_list(cls, name_list):
        current_division_tree = cls._division_tree
        result_division_code = None

        for name in name_list:
            for division_code, division_name_list, next_division_tree in current_division_tree:
                if name in division_name_list:
                    current_division_tree = next_division_tree
                    result_division_code = division_code
                    break
            else:
                return None
        return result_division_code


class DeprecatedDivision(Division):
    _division_tree = simplejson.loads(resource_string(__name__, 'data/deprecated_division.json'))
    _jd_division_mappings = simplejson.loads(resource_string(__name__, 'data/deprecated_jd_division_mappings.json'))
    _jd_division = simplejson.loads(resource_string(__name__, 'data/deprecated_jd_division.json'))
    version = 'v1'
    is_latest_version = False


class LatestDivision(Division):
    _division_tree = simplejson.loads(resource_string(__name__, 'data/division.json'))
    _jd_division_mappings = simplejson.loads(resource_string(__name__, 'data/jd_division_mappings.json'))
    _jd_division = simplejson.loads(resource_string(__name__, 'data/jd_division.json'))
    version = 'v2'
    is_latest_version = True


DIVISION_MAPPINGS = {'v1': DeprecatedDivision, 'v2': LatestDivision}
