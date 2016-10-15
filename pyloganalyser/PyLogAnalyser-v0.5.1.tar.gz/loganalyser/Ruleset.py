#!/usr/bin/python
# -*- coding: ascii -*-
"""
\brief      Module which contains Ruleset class.
\author     imoren2x
\copyright  CC BY-NC-SA 4.0
"""

import re
from ConfigParser import RawConfigParser
from Rule import Rule
from logs.loggers import LOGGER_RULESET


class Ruleset(object):
    """
    Class instantiated by PyLogAnalyser.py using the configuration
    file which parses all the rules, establishes if the input line
    matches or not the rules and it returns the output log line to
    be used by the handlers.
    """

    def __init__(self, config_file):
        """
        """
        #
        self._logger = LOGGER_RULESET
        self._logger.info("*** class Ruleset BEGIN ***")
        #
        self.__conf_file = config_file
        #Ruleset contains a list of rules.
        self.__ruleset = list([])
        self.__match_rule = None
        self.__rule_titles = list([])

        #Open and parse configuration File.
        self.__config_parser = RawConfigParser()
        self.__config_parser.readfp(open(config_file))
        self._logger.verbose("Configuration file prepared")

        self.__parse_config_file()
        self._logger.debug("Configuration file parsed")

        self.__set_default_rule()
        self._logger.debug("Default rule set")

    def __str__(self):
        """
        Display the ruleset.
        """
        ruleset_str = "\n"
        rule_separator = "\n-------\n"

        for rule in self.__ruleset:
            ruleset_str += str(rule) + rule_separator

        ruleset_str += "Match rule: " + str(self.__match_rule)

        return str(ruleset_str)

    def match(self, line, line_number=0):
        """
        """
        self._logger.debug("Ruleset match begins")

        #print self.__rule_titles
        for rule in self.__ruleset:
            if bool(rule.match(line, line_number)):
                self.__match_rule = rule
                msg = "Line matched with Rule %s!" % self.__match_rule.get_title()
                self._logger.debug(msg)
                return True

        self._logger.debug("Line did not match!")
        return False

    def get_output(self, line, line_number=0):
        """
        @rtype: String or None.
        """
        #FIXME: this method should contain better definition
        self._logger.debug("Ruleset get output begins")
        self._logger.debug("Line: %s" % str(line))
        self._logger.debug("Line number: %s" % str(line_number))
        match_result = self.match(line, line_number)
        if bool(match_result):
            return self.__match_rule.get_output(line, line_number)
        elif not bool(match_result):
            return None
        elif bool(match_result) is None:
            raise Exception("This line doesn't match any rule. Not admissible. Please, check.")

    def get_match_rule(self):
        """
        """
        return str(self.__match_rule)

    def __parse_config_file(self):
        """
        Parse configuration file, containing the
        ruleset with all the rules to parse.
        """
        sections = self.__config_parser.sections()
        self._logger.debug("Sections: %s" % str(sections))

        self.__check_rule_duplicity(sections)

        self.__rule_titles = self.__get_list_of_rules(sections)

        self._logger.debug("Rule titles: %s" % str(self.__rule_titles))
        for rule_title in self.__rule_titles:
            self.__set_rule(rule_title, self.__config_parser.items(rule_title))

    def __get_list_of_rules(self, sections):
        """
        """
        list_of_rules = list([])

        # Check includeOnly
        incl_only = False
        incl_only_list = map(self.__check_incl_only, sections)
        if True in incl_only_list:
            incl_only = True
            index = incl_only_list.index(bool(True))
            incl_only_section = sections[index]
            rule = Rule(incl_only_section, self.__config_parser.items(incl_only_section))

            if rule.is_active():
                return rule.get_include_list()

            # If present but not active, consider as False.
            incl_only = False

        #Remove non-process rules
        #FIXME: remove all of this and let only
        #  a self.__is_not_process_rule(section)
        #  to filter unnecessary rules.
        regex_include_only = re.compile(Rule.INCLUDEONLY_re_str)
        regex_function = re.compile(Rule.FUNCTION_NAME_re_str)
        regex_template = re.compile(Rule.TEMPLATE_NAME_re_str)
        regex_exclude_only = re.compile(Rule.EXCLUDEONLY_re_str)
        for section in sections:
            section_lower = section.lower()
            match_include_only = regex_include_only.match(section_lower)
            match_function = regex_function.match(section_lower)
            match_template = regex_template.match(section_lower)
            match_exclude_only = regex_exclude_only.match(section_lower)
            if not(match_include_only) and \
                not(match_function) and \
                not(match_template) and \
                not(match_exclude_only):
                #
                list_of_rules.append(section)

        #Check excludeOnly
        excl_only_list = map(self.__check_excl_only, sections)
        if (True in excl_only_list) and not(incl_only):
            index = excl_only_list.index(bool(True))
            excl_only_section = sections[index]
            rule = Rule(excl_only_section, self.__config_parser.items(excl_only_section))

            if rule.is_active():
                exclude_list = rule.get_exclude_list()

                for exclude_rule in exclude_list:
                    list_of_rules.remove(exclude_rule)

        return list_of_rules

    def __check_rules_only(self, section, regex_str):
        """
        @rtype True if matches, False otherwise.
        """
        regex_include_only = re.compile(regex_str)
        result = None

        section_lower = section.lower()
        if regex_include_only.match(section_lower):
            self._logger.debug("Only-like rule found")
            result = True
        else:
            self._logger.debug("No Only-like rule")
            result = False

        return result

    def __check_incl_only(self, section):
        """
        """
        return self.__check_rules_only(section, Rule.INCLUDEONLY_re_str)

    def __check_excl_only(self, section):
        """
        @rtype tuple(bool, int)
        """
        return self.__check_rules_only(section, Rule.EXCLUDEONLY_re_str)

    def __check_rule_duplicity(self, rules):
        """
        @param rules: list of rules to process.
        @type rules: list of strings
        """
        for rule in rules:
            if rules.count(rule) > 1:
                raise Exception("One rule is duplicated, please check.\n" \
                    + " Rule: %s" % str(rule))

        self._logger.debug("No rule duplicity")

    def __set_rule(self, section, items):
        """
        To substitute __set_rule (verify also)
            because it uses templates.
        """
        self._logger.debug("Set new rule in ruleset - begins")
        #self._logger.verbose("Rule title: %s" % str(section))
        #self._logger.verbose("Rule Items: %s" % str(items))
        #
        final_items = list([])
        final_items = items

        if Rule.FUNCTION_NAME in dict(items).keys():
            self._logger.verbose("Function in items of rule \'%s\'" % str(section))
            #Get function title
            function_title = dict(items)[Rule.FUNCTION_NAME]
            self._logger.verbose("Function rule title: %s" % str(function_title))
            #Get sections
            sections = self.__config_parser.sections()

            if function_title not in sections:
                raise Exception("%s \"%s\" is not present " % (Rule.FUNCTION_NAME, function_title) \
                + "in sections %s .\n" % sections \
                + "Please, check.")

            function_items = self.__config_parser.items(function_title)
            self._logger.verbose("Function rule items: %s" % str(function_items))

            #Check that no items are returned.
            final_items = self.__merge_rule_elements(final_items, function_items)

        if Rule.TEMPLATE_NAME in dict(items).keys():
            self._logger.debug("Template in items of rule \'%s\'" % str(section))
            #Get function title
            template_title = dict(items)[Rule.TEMPLATE_NAME]
            self._logger.debug("Template rule title: %s" % str(template_title))
            #Get sections
            sections = self.__config_parser.sections()

            if template_title not in sections:
                raise Exception("%s \"%s\" is not present " % (Rule.TEMPLATE_NAME, template_title) \
                    + "in sections %s .\n" % sections \
                    + "Please, check.")

            template_items = self.__config_parser.items(template_title)
            self._logger.debug("Template rule items: %s" % str(template_items))
            #Check that no items are returned.
            final_items = self.__merge_rule_elements(final_items, template_items)

        rule = Rule(section, final_items)

        self.__ruleset.append(rule)
        self._logger.debug("Rule appended")

    def __merge_rule_elements(self, items_prio, items_sec):
        """
        items = [(key, value) ... ]
        """
        self._logger.verbose("Rule item merging - begins")
        result_items = list([])

        dict1 = dict(items_prio)
        keys1 = dict1.keys()
        dict2 = dict(items_sec)
        keys2 = dict2.keys()

        #Merge keys
        keys = list(set(keys1 + keys2))

        for key in keys:
            value = None
            if dict1.has_key(key):
                value = dict1[key]
            elif dict2.has_key(key):
                value = dict2[key]

            item = tuple((key, value))
            result_items.append(item)

        self._logger.verbose("Rule item merging - ends")
        return result_items

    def __set_default_rule(self):
        """
        """
        self._logger.verbose("Set default rule - begins")
        sections = self.__config_parser.sections()

        #If DEF_SECTION already present, don't include it.
        if Rule.DEFAULT_RULE_NAME in sections:
            self._logger.debug("Default rule already set")
            return

        #Otherwise, include it:
        rule = Rule(Rule.DEFAULT_RULE_NAME, Rule.DEFAULT_ITEMS)
        self._logger.debug("Default rule set")

        self.__ruleset.append(rule)
        self._logger.debug("Default rule appended")

    def __del__(self):
        """
        Destructor
        """
        self._logger.info("*** class Ruleset END ***")
