from builtins import str
from builtins import object
import re
import uuid
from tag_processor.models import *
from tag_processor.services import execute_tag_chain


class TagParser(object):

    def __init__(self, data_container):
        self.data_container = data_container

    # deprecated
    def parse(self, input_string):
        result = list()

        if not input_string:
            return result

        all_tags = self.parse_levels(input_string)
        for tag_level in reversed(list(all_tags.keys())):
            tags = all_tags[tag_level]
            for tag in tags:
                elements = self.get_elements(tag)
                result.append({
                    'text': tag,
                    'chain': elements
                })

        return result

    def parse_levels(self, input_string):
        return self._get_tags(input_string)

    def parse_level(self, input_string):
        tags = self._get_tags(input_string)
        if not tags:
            return None
        return tags[len(tags.keys()) - 1]

    def get_elements(self, input_string):
        if '|' in input_string:
            return [self.get_disjunction_tag(input_string.split(u'|'))]
        if input_string.count("?") > input_string.count("\?"):
            return [self.get_ternary_tag(input_string)]
        elements = self._split_by_elements(input_string)
        elements = self._split_attributes(elements)
        return [self._box_element(element) for element in elements]

    @staticmethod
    def _split_by_elements(input_string):
        # "warehouse__storage[max=cargo__quantity]__name"
        brace_opened = False
        underscores_index = -1
        elements = []
        for i, c in enumerate(input_string):
            if i == len(input_string) - 1:
                elements.append(input_string[underscores_index+1:i+1])
            elif c == '[':
                brace_opened = True
            elif c == ']':
                brace_opened = False
            elif c == '_' and input_string[i+1] == '_' and not brace_opened:
                elements.append(input_string[underscores_index+1:i])
                underscores_index = i+1

        return elements

    @staticmethod
    def _get_tags(input_string):
        tags = {}
        level = -1
        iterators = {
            0: 0
        }
        for i, c in enumerate(input_string):
            if c == '$' and input_string[i+1] == '{':
                iterators[level + 1] = i+2
                level += 1

            if c == '}':
                tags.setdefault(level, []).append(input_string[iterators[level]:i])
                level -= 1

        return tags

    def _box_element(self, element):
        if element[0] == '[' and element[-1] == ']':
            return self.get_function_tag(element)
        return self.get_object_tag(element)

    def get_function_tag(self, element):
        function_elements = element[1:-1].split('=')
        function = getattr(self.data_container, function_elements[0], None)
        params = None
        if len(function_elements) > 1:
            params = function_elements[1]
        return FunctionTag(function, params)

    @staticmethod
    def get_object_tag(element):
        return ObjectTag(element)

    def get_ternary_tag(self, input_string):
        condition, if_true, if_false = self._parse_ternary_operator(input_string)
        condition_elements = self.get_elements(condition)
        return TernaryTag(condition_elements, ConstantTag(if_true), ConstantTag(if_false))

    @staticmethod
    def get_disjunction_tag(elements):
        disjunction_elements = []
        for element in elements:
            disjunction_elements.append(ConstantTag(element))
        return DisjunctionTag(disjunction_elements)

    @staticmethod
    def _split_attributes(elements):
        result = []
        for raw_element in elements:
            attributes = re.findall("[^\[\];]+(?=[;\]])", raw_element)

            element_without_attribute = re.search("[^\[\]]+(?=[\[])", raw_element)
            element = raw_element
            if element_without_attribute:
                element = element_without_attribute.group(0)

            result.append(element)
            if attributes:
                for attribute in attributes:
                    result.append('[' + attribute + ']')

        return result

    @staticmethod
    def _parse_ternary_operator(input_string):
        temp_string = input_string.replace("\:", "--")
        question_index = temp_string.index("?")
        colon_index = temp_string.index(":")
        return input_string[0:question_index], input_string[question_index+1:colon_index], input_string[colon_index+1:]


class TagProcessor(object):

    tag_parser = None
    __internal_container = None

    def __init__(self, data_container):
        self.__internal_container = dict()
        self.data_container = data_container
        self.tag_parser = TagParser(self.data_container)

    def execute(self, input_string):
        low_level_tags = self.tag_parser.parse_level(input_string)
        while low_level_tags is not None:
            parsed_tags = []
            for tag_level in low_level_tags:
                elements = self.tag_parser.get_elements(tag_level)
                parsed_tags.append({
                    'text': tag_level,
                    'chain': elements
                })
            input_string = self.execute_tags(input_string, parsed_tags)
            low_level_tags = self.tag_parser.parse_level(str(input_string))
        return self.__process_keys(input_string)

    def execute_tags(self, input_string, tags):
        for tag in tags:
            tag_text = "${" + tag.get('text') + "}"
            tag_result = self.process_tag(tag)
            tag_hash = self.__save_intermediate_result(tag_result)
            input_string = input_string.replace(tag_text, tag_hash)
        return input_string

    def process_tag(self, tag):
        self.data_container.update(self.__internal_container)
        return execute_tag_chain(tag.get('chain', None), self.data_container)

    def __save_intermediate_result(self, result):
        if result is None:
            result = u''

        if self.__internal_container.get(result) is not None:
            return result

        key = self._generate_key()
        self.__internal_container[key] = result
        return key

    @staticmethod
    def _generate_key():
        return str(uuid.uuid4())[:8]

    def __process_keys(self, input_string):
        for key, value in self.__internal_container.items():
            if input_string == key and not self.__has_other_keys(self.__internal_container, key, input_string.replace(key, str(value))):
                return value

            if key in input_string:
                self.__internal_container.pop(key, None)
                return self.__process_keys(input_string.replace(key, str(value)))
        return input_string

    @staticmethod
    def __has_other_keys(dict, existing_key, input_string):
        for key in dict.keys():
            if existing_key != key and key in input_string:
                return True
        return False
