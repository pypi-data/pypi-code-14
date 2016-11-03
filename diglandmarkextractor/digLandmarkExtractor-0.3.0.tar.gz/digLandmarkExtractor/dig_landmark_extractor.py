# -*- coding: utf-8 -*-
"""Module for defining an extractor that accepts a list of tokens
and outputs tokens that exist in a user provided trie"""
import copy

from digExtractor.extractor import Extractor
from landmark_extractor.extraction.Landmark import Rule, RuleSet


class DigLandmarkExtractor(Extractor):

    def __init__(self):
        self.renamed_input_fields = 'html'
        self.rule = None
        self.rule_set = None

    def get_rule(self):
        return self.rule

    def set_rule(self, rule):
        if not isinstance(rule, Rule):
            raise ValueError("rule must be a Rule")
        self.rule = rule
        return self

    def get_rule_set(self):
        return self.rule_set

    def set_rule_set(self, rule_set):
        if not isinstance(rule_set, RuleSet):
            raise ValueError("rule_set must be a RuleSet")
        self.rule_set = rule_set
        return self


    def flattenResult(self, extraction_object, name = 'root'):
        result = {}
        if isinstance(extraction_object, dict):
            if 'sub_rules' in extraction_object:
                for item in extraction_object['sub_rules']:
                    result[item] = self.flattenResult(extraction_object['sub_rules'][item], item)
            elif 'sequence' in extraction_object:
                result = self.flattenResult(extraction_object['sequence'], 'sequence')
            elif 'extract' in extraction_object:
                if self.get_include_context():
                    return self.convert_result(extraction_object)
                else:
                    return extraction_object['extract']
            else:
                for extract in extraction_object:
                    result[extract] = self.flattenResult(extraction_object[extract], extract)

        if isinstance(extraction_object, list):
            result = []
            for extract in extraction_object:
                result.append(self.flattenResult(extract, 'sequence'))
        return result

    def convert_result(self, result):
        if not result['extract']:
            return ""
        return self.wrap_value_with_context(result['extract'],
                                            'html',
                                            result['begin_index'],
                                            result['end_index'])

    def extract(self, doc):
        if self.rule is not None:
            html = doc['html']
            result = self.rule.apply(html)
            result = self.flattenResult(result)
            return result
        elif self.rule_set is not None:
            result = dict()
            html = doc['html']
            for rule in self.rule_set.rules:
                rule_result = rule.apply(html)
                rule_result = self.flattenResult(rule_result)
                if rule_result:
                    if rule.name not in result:
                        result[rule.name] = rule_result
                    elif isinstance(result[rule.name], list):
                        result[rule.name].append(rule_result)
                    else:
                        result[rule.name] = [result[rule.name], rule_result]

            return result

    def get_metadata(self):
        """Returns a copy of the metadata that characterizes this extractor"""
        return copy.copy(self.metadata)

    def set_metadata(self, metadata):
        """Overwrite the metadata that characterizes this extractor"""
        self.metadata = metadata
        return self

    def get_renamed_input_fields(self):
        """Return a scalar or ordered list of fields to rename to"""
        return self.renamed_input_fields
