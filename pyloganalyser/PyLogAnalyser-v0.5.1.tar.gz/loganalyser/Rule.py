#!/usr/bin/python
# -*- coding: ascii -*-
"""
\brief      Module which contains the Rule class.
\author     imoren2x
\copyright  CC BY-NC-SA 4.0
"""

import re
import datetime
from LogLine import LogLine
from logs.loggers import LOGGER_RULE
from __init__ import __version__


class Rule(object):
    """
    Class instantiated by Ruleset class using the rule
    title and the list of key-value pairs.
    Also, it returns True or False if an input line matches
    the rule, and the output of the rule.
    """

    #Title
    TITLE           = "title"
    VERSION         = __version__

    #Type of rule values
    # related to self.__type_of_rule
    TYPE_OF_RULE       = str("type of rule")
    INCLUDEONLY        = str("includeonly")
    INCLUDEONLY_re_str = str("includeonly|include only")
    EXCLUDEONLY        = str("excludeonly")
    EXCLUDEONLY_re_str = str("excludeonly|exclude only")
    FUNCTIONRULE_str   = str("function")
    STDRULE_str        = str("stdrule")
    EXCLUDE_list       = str("exclude list")
    INCLUDE_list       = str("include list")

    #
    REGEX_NAME        = "regex"
    MATCH_SEARCH_NAME = "match_search" #(default: match)
    MATCH_SEARCH_str1 = "match"
    MATCH_SEARCH_str2 = "search"
    REGEX_FLAGS       = "regex_flags"

    ACTION_NAME     = "action"

    DATE_str        = "date"
    DATE_REGEX_str  = "date_regex"
    DATE_MIN_str    = "date_min"
    DATE_MAX_str    = "date_max"
    DATE_FORMAT_str = "date_format"

    #
    LINE_NUM_AFTER_MIN  =  1
    LINE_NUM_BEFORE_MAX = -1
    #LINE_AFTER_str      = "line after"
    LINE_AFTER_str      = "line_min"
    #LINE_BEFORE_str     = "line before"
    LINE_BEFORE_str     = "line_max"

    #Active or disabled values
    ACTIVE_NAME      = "active"
    ACTIVE           = True
    DISABLED         = False
    ACTIVE_NAMES     = "yes|true|no|false"
    ACTIVE_NAMES_pos = "yes|true"
    ACTIVE_NAMES_neg = "no|false"

    #Highlight names:
    HIGHLIGHT_FG_NAME = "hl_fg"
    HIGHLIGHT_BG_NAME = "hl_bg"

    #Columnize name:
    COLUMNIZE_NAME = "columnize"

    #Template_name:
    TEMPLATE_NAME = "template"
    TEMPLATE_NAME_re_str = "^template .*$"

    #Function name:
    FUNCTION_NAME = "function"
    FUNCTION_NAME_re_str = "^function .*$"
    FUNCTION_PATH = "path"
    FUNCTION_MODULE = "module"
    FUNCTION_TO_EXE = "method"
    FUNCTION_ARGS = tuple(())
    FUNCTION_ARGS_NAME = "args"

    #Regex_ids
    REGEX_IDS = "regex ids"

    #Reserved words
    NON_REGEX_IDS_list = [REGEX_NAME, ACTION_NAME, ACTIVE_NAME, \
        DATE_str, DATE_MIN_str, DATE_MAX_str, DATE_FORMAT_str, \
        MATCH_SEARCH_NAME, REGEX_FLAGS, LINE_AFTER_str, \
        LINE_BEFORE_str, HIGHLIGHT_FG_NAME, HIGHLIGHT_BG_NAME, \
        COLUMNIZE_NAME, TEMPLATE_NAME, FUNCTION_NAME, \
        FUNCTION_PATH, FUNCTION_MODULE, FUNCTION_TO_EXE, \
        FUNCTION_ARGS_NAME]

    #Action values
    FILTER   = str("filter")
    PASS     = str("pass")
    ACTION_NAMES = "filter|pass"

    #Default rule
    DEFAULT_RULE_NAME = "DEFAULT_RULE"
    DEFAULT_ACTION = FILTER
    DEFAULT_regex_str = ".*"
    DEFAULT_ITEMS = list([tuple((REGEX_NAME, DEFAULT_regex_str)), \
        tuple((ACTIVE_NAME, str(ACTIVE))), \
        tuple((ACTION_NAME, DEFAULT_ACTION))])

    def __init__(self, title, rule_elements):
        """
        Constructor for the Rule.

        @param title: Title of the rule.
        @type title: string

        @param rule_elements: list of (name, value) pairs containing
            the rule elements to be considered.
        @type rule_elements: list of (name, value) pairs.
        """
        #
        self._logger = LOGGER_RULE
        self._logger.verbose("*** class Rule BEGIN ***")
        #
        self._logger.debug("Title: %s" % str(title))
        self._logger.debug("Rule Elements: %s" % str(rule_elements))

        #Initialization
        self.__title         = None
        self.__type_of_rule  = None
        self.__action        = None
        self.__active        = None
        self.__rule_elements = None

        self.__regex_str    = None
        self.__regex_flags  = None
        self.__match_search = None

        self.__line_num_before = None
        self.__line_num_after  = None

        self.__rule_ids     = dict({})

        self.__highlight_FG = None
        self.__highlight_BG = None

        self.__date_regex   = None
        self.__date_format  = None
        self.__date_min     = None
        self.__date_max     = None
        self.__datetime_factory = datetime.datetime(1970, 1, 1)

        self.__columnize = None

        self.__template = None

        self.__function = dict({})

        self.__exclude_list = list([])
        self.__include_list = list([])

        #Setting values according to rule_elements
        self.__title = title
        self.__rule_elements = rule_elements
        self.__set_type_of_rule()

        #Set default values
        self.__set_default_values()
        self._logger.debug("Default values set")

        #Depending, parse includeOnly, exclude_only or filterset.
        if self.__type_of_rule == Rule.INCLUDEONLY:
            self.__set_include_list(rule_elements)
        elif self.__type_of_rule == Rule.EXCLUDEONLY:
            self.__set_exclude_list(rule_elements)
        else:
            self.__set_std_rule(rule_elements)

        self.__check_at_least_one_rule()

    def __str__(self):
        """
        """
        LEN = 15
        #TODO: improve presentation.
        out_title        = "%s %s" % (("%s:" % Rule.TITLE).ljust(LEN), self.__title)
        out_type_of_rule = "%s %s" % (("%s:" % Rule.TYPE_OF_RULE).ljust(LEN), self.__type_of_rule)
        out_active       = "%s %s" % (("%s:" % Rule.ACTIVE_NAME).ljust(LEN), self.__active)
        out_action       = "%s %s" % (("%s:" % Rule.ACTION_NAME).ljust(LEN), self.__action)
        out_regex        = "%s %s" % (("%s:" % Rule.REGEX_NAME).ljust(LEN), self.__regex_str)
        out_regex_flags  = "%s %s" % (("%s:" % Rule.REGEX_FLAGS).ljust(LEN), self.__regex_flags)
        out_regex_match_search = "%s %s" % (("%s:" % Rule.MATCH_SEARCH_NAME).ljust(LEN), self.__match_search)
        out_line_before  = "%s %s" % (("%s:" % Rule.LINE_AFTER_str).ljust(LEN), self.__line_num_after)
        out_line_after   = "%s %s" % (("%s:" % Rule.LINE_BEFORE_str).ljust(LEN), self.__line_num_before)
        out_date_regex = "%s %s" % (("%s:" % Rule.DATE_REGEX_str).ljust(LEN), self.__date_regex)
        out_line_date_min = "%s %s" % (("%s:" % Rule.DATE_MIN_str).ljust(LEN), self.__date_min)
        out_line_date_max = "%s %s" % (("%s:" % Rule.DATE_MAX_str).ljust(LEN), self.__date_max)
        out_line_date_format = "%s %s" % (("%s:" % Rule.DATE_FORMAT_str).ljust(LEN), self.__date_format)
        out_line_highlight_fg = "%s %s" % (("%s:" % Rule.HIGHLIGHT_FG_NAME).ljust(LEN), self.__highlight_FG)
        out_line_highlight_bg = "%s %s" % (("%s:" % Rule.HIGHLIGHT_BG_NAME).ljust(LEN), self.__highlight_BG)
        out_line_columnize = "%s %s" % (("%s:" % Rule.COLUMNIZE_NAME).ljust(LEN), self.__columnize)
        out_line_template = "%s %s" % (("%s:" % Rule.TEMPLATE_NAME).ljust(LEN), self.__template)
        out_exclude_list = "%s %s" % (("%s:" % Rule.EXCLUDE_list).ljust(LEN), str(self.__exclude_list))
        out_include_list = "%s %s" % (("%s:" % Rule.INCLUDE_list).ljust(LEN), str(self.__include_list))

        rule_ids_keys = self.__rule_ids.keys()
        rule_ids_str = ""
        for key in rule_ids_keys:
            rule_id = "%s %s \n" % (("%s:" % key).ljust(LEN), self.__rule_ids[key])
            rule_ids_str += rule_id

        # func_ids_keys = self.__function.keys()
        # func_ids_str = ""
        # for key in func_ids_keys:
            # func_id = "%s: %s \n" % (key, self.__function[key])
            # func_ids_str += func_id

        out = out_title + "\n" + \
            out_type_of_rule + "\n" + \
            out_active + "\n" + \
            out_action + "\n" + \
            out_regex + "\n" + \
            out_regex_flags + "\n" + \
            out_regex_match_search + "\n" + \
            rule_ids_str + \
            out_line_highlight_fg + "\n" + \
            out_line_highlight_bg + "\n" + \
            out_line_before + "\n" + \
            out_line_after + "\n" + \
            out_line_date_min + "\n" + \
            out_line_date_max + "\n" + \
            out_line_date_format + "\n" + \
            out_line_columnize + "\n" + \
            out_line_template + "\n" + \
            out_exclude_list + "\n" + \
            out_include_list

        return str(out)

    def get_title(self):
        """
        """
        return self.__title

    def match(self, line, line_number = 0):
        """
        Takes the line and checks if it matches or not.

        @return True if match and active, False otherwise.
        @rtype: Boolean.
        """
        self._logger.debug("Input line: %s" % str(line.strip()))
        self._logger.debug("Input line number: %s" % str(line_number))
        match_result = None
        match_list   = list([])

        #Local parameters for easier reading
        match_regex     = self.__match_regex(line)
        rule_ids_keys   = self.__rule_ids.keys()
        match_active    = self.__active
        regex_str       = self.__regex_str

        #Condition to check that at least one
        #   rule_id is present
        rule_ids_exist = (len(rule_ids_keys) > 0)

        date_ids_exist = self.__date_ids_exist()

        line_number_exist = (self.__line_num_before < Rule.LINE_NUM_BEFORE_MAX) or \
            (self.__line_num_after > Rule.LINE_NUM_AFTER_MIN)

        #Match lines
        match_lines = self.__match_line_number(line_number)

        if match_active and (match_regex or match_lines):
            self._logger.debug("Rule active")
            if rule_ids_exist:
                self._logger.debug("Match rule ids")
                match_rule_ids_list  = self.__match_rule_ids(line)
                match_list          += match_rule_ids_list

            if date_ids_exist:
                self._logger.debug("Match date ids")
                match_datetime = self.__match_datetime(line)
                match_list.append(match_datetime)

            match_list.append(match_regex)

            if line_number_exist:
                match_list.append(match_lines)

            self._logger.debug("List of matches: %s" % str(match_list))
        else:
            self._logger.debug("Rule non-active or non-matching")
            match_result = False

        #Filter Non-Applicable results
        match_filtered_list = [element for element in match_list if element != None]
        self._logger.debug("Filtered list of matches: %s" % str(match_filtered_list))

        if len(match_filtered_list) > 1:
            self._logger.debug("Reducing match list")
            match_result = reduce(lambda x, y: x and y, match_list)
        elif len(match_filtered_list) > 0:
            self._logger.debug("Taking match result")
            match_result = match_filtered_list[0]

        self._logger.debug("Rule match result: %s - ends" % str(match_result))
        return match_result

    def __date_ids_exist(self):
        """
        """
        result = None

        date_regex  = self.__date_regex
        date_format = self.__date_format
        date_min    = self.__date_min
        date_max    = self.__date_max

        condition_1 = date_regex is not None
        condition_2 = date_format is not None
        condition_3 = (date_max is not None) or \
                        (date_min is not None)

        result = condition_1 and condition_2 \
                    and condition_3

        return result

    def __match_regex(self, line):
        """
        """
        #Take local variables
        regex_str    = str(self.__regex_str)
        #regex_flags  = self.__regex_flags if (self.__regex_flags is not None) else 0
        regex_flags  = self.__regex_flags
        match_search = str(self.__match_search)

        result = None
        if match_search == Rule.MATCH_SEARCH_str1:
            result = bool(re.match(regex_str, line, regex_flags))
        elif match_search == Rule.MATCH_SEARCH_str2:
            result = bool(re.search(regex_str, line, regex_flags))
        else:
            msg = "%s parameter has an abnormal value \"%s\"." % (Rule.MATCH_SEARCH_NAME, str(match_search))
            raise Exception(msg)

        return result

    def __match_line_number(self, line_number):
        """
        TODO: I should consider None results
        """
        result_line_after  = None
        result_line_before = None

        if line_number >= self.__line_num_after:
            result_line_after = True
        else:
            result_line_after = False

        cond_1 = (line_number <= self.__line_num_before)
        cond_2 = (self.__line_num_before == Rule.LINE_NUM_BEFORE_MAX)
        if cond_1 or cond_2:
            result_line_before = True
        else:
            result_line_before = False

        return (result_line_after and result_line_before)

    def __match_rule_ids(self, line):
        """
        It takes all the elements from rule_ids
         and creates a True/False list if it matches or not.

        Returns this list.
        """
        match_list = list([])
        rule_ids_keys = self.__rule_ids.keys()
        regex_str     = self.__regex_str

        self.__check_regex_ids()

        match_object = re.match(regex_str, line)

        for key in rule_ids_keys:
            value = self.__rule_ids[key]
            match_rule_key = self.__match_rule_id(key, value, match_object)
            match_list.append(match_rule_key)

        return match_list

    def __check_regex_ids(self):
        """
        """
        rule_ids_keys = self.__rule_ids.keys()
        #
        for rule_id_key in rule_ids_keys:
            if rule_id_key in Rule.NON_REGEX_IDS_list:
                msg = "Identifier %s can't be used as group name inside the regular expression. Please, use a non-reserved word" % str(rule_id_key)
                raise Exception(msg)

    def __match_rule_id(self, key, value, match_object):
        """
        Return True if match, False if it does not match.
        It is not possible to raise an exception because it is checked
         previously in
        """
        if match_object is None:
            return False

        line_value = match_object.group(key)

        #return True if (line_value == value) else False
        return True if (re.match(value, line_value)) else False

    def __match_datetime(self, line):
        """
        Returns True of False depending of.
        """
        match_result = None

        regex_str   = self.__regex_str
        date_min    = self.__date_min
        date_max    = self.__date_max
        date_format = self.__date_format
        factory     = self.__datetime_factory

        datetime_min = None
        datetime_max = None
        #
        if date_min is not None:
            datetime_min = factory.strptime(date_min, date_format)

        if date_max is not None:
            datetime_max = factory.strptime(date_max, date_format)

        #
        regex       = re.compile(regex_str)
        match_obj   = regex.match(line)
        if match_obj is None:
            return False
        date_line   = match_obj.group(Rule.DATE_str)
        datetime_line = factory.strptime(date_line, date_format)
        #
        if datetime_min is None:
            match_result = (datetime_line <= datetime_max)
        elif datetime_max is None:
            match_result = (datetime_line >= datetime_min)
        else:
            match_result = (datetime_line >= datetime_min) \
                and (datetime_line <= datetime_max)

        return match_result

    def get_output(self, line, line_number = 0):
        """
        @rtype: String.
        """
        self._logger.debug("Rule output begins")
        self._logger.debug("Line: %s" % str(line))
        self._logger.debug("Line number: %s" % str(line_number))
        result = None

        action       = self.__action
        type_of_rule = self.__type_of_rule
        columnize    = self.__columnize
        function     = self.__function

        if action == Rule.FILTER:
            self._logger.debug("Rule action is filter.")
            result = None
        elif self.match(line, line_number) and \
            action == Rule.PASS:
            #
            self._logger.debug("Line/Line number match")
            self._logger.debug("Rule action is pass")
            highlight_FG = self.__highlight_FG
            highlight_BG = self.__highlight_BG
            if columnize is not None:
                line = self.__columnize_line(line)
                self._logger.debug("Columnized line: %s" % str(line))
            elif function != dict({}):
                line = self.__function_line(line)
                self._logger.debug("Processed line: %s" % str(line))

            self._logger.debug("Generating log line")
            logLine = LogLine(string = line, \
                                color_fg = highlight_FG, \
                                color_bg = highlight_BG)
            result = logLine

        #self._logger.debug("Rule output result: %s. ends" % str(result))
        return result

    def __columnize_line(self, line):
        """
        """
        self._logger.debug("Columnize line begins")
        column_keys = self.__columnize.keys()
        output_line = ""
        regex_str = self.__regex_str

        for group_index in column_keys:
            #Length of the output field
            output_len = self.__columnize[group_index]
            #Take the input field and length
            input_field = re.match(regex_str, line).group(group_index)
            input_len = len(input_field.strip())
            #Take the initial output field
            output_field = self.__columnize_field(input_field.strip(), output_len) if output_len > input_len \
                           else input_field.strip()

            output_line += output_field + " "

        #Include return at the end
        output_line += "\n"

        return output_line

    def __columnize_field(self, input_field, output_len):
        """
        """
        output_field = None

        if input_field.isdigit():
            output_field = input_field.rjust(output_len)
        else:
            output_field = input_field.ljust(output_len)

        return output_field

    def __function_line(self, input_line):
        """
        Transforms input line and returns output line.
        """
        path     = self.__function[Rule.FUNCTION_PATH]
        module   = self.__function[Rule.FUNCTION_MODULE]
        function = self.__function[Rule.FUNCTION_NAME]
        args     = self.__function[Rule.FUNCTION_ARGS_NAME]

        output_line = None

        #convert values
        line = input_line

        #Add path to PYTHONPATH:
        import sys
        sys.path.append(path)
        exec("import %s" % module)
        function_to_exe = "output_line = %s.%s(%s)" % (module, function, str(args))
        #print function_to_exe
        exec(function_to_exe)

        return output_line

    def __set_default_values(self):
        """
        """
        self.__active           = Rule.ACTIVE
        self.__action           = Rule.PASS
        self.__line_num_before  = Rule.LINE_NUM_BEFORE_MAX
        self.__line_num_after   = Rule.LINE_NUM_AFTER_MIN
        self.__regex_flags      = 0
        self.__match_search     = Rule.MATCH_SEARCH_str1

        #TODO: add new default values

    def is_active(self):
        """
        """
        return self.__active

    def __set_std_rule(self, rule_elements):
        """
        """
        for element in rule_elements:
            self._logger.debug("Rule element to set: %s" % str(element))
            self.__set_rule_element(element)

    def __set_rule_element(self, element):
        """
        """
        #Convert into dictionary and extract key and value
        # elem_dict = dict(list([element]))
        # key = str(elem_dict.keys()[0].lower())
        # value = str(elem_dict.values()[0])
        key = str(element[0].lower())
        value = str(element[1])
        self._logger.debug("key/value: %s / %s" % (str(key), str(value)))

        #Date: include new checks.
        self.__check_rule_element(key, value)

        if key == Rule.REGEX_NAME:
            self.__regex_str = value
            self._logger.debug("%s set with %s" % (Rule.REGEX_NAME, value))
        elif key == Rule.MATCH_SEARCH_NAME:
            self.__match_search = value
            self._logger.debug("%s set with %s" % (Rule.MATCH_SEARCH_NAME, value))
        elif key == Rule.REGEX_FLAGS:
            exec("regex_flags = %s" % str(value))
            self.__regex_flags = regex_flags
            self._logger.debug("%s set with %d" % (Rule.REGEX_FLAGS, regex_flags))
        elif key == Rule.ACTIVE_NAME:
            self.__set_rule_element_active(value)
            self._logger.debug("%s set with %s" \
                % (Rule.ACTIVE_NAME, self.__active))
        elif key == Rule.ACTION_NAME:
            self.__action = value.lower()
            self._logger.debug("%s set with %s" \
                % (Rule.ACTION_NAME, self.__action))
        elif key == Rule.LINE_AFTER_str:
            self.__line_num_after = int(value)
            self._logger.debug("%s set with %s" \
                % (Rule.LINE_AFTER_str, self.__line_num_after))
        elif key == Rule.LINE_BEFORE_str:
            self.__line_num_before = int(value)
            self._logger.debug("%s set with %s" \
                % (Rule.LINE_BEFORE_str, self.__line_num_before))
        elif key == Rule.DATE_MIN_str:
            self.__date_min = str(value)
            self._logger.debug("%s set with %s" \
                % (Rule.DATE_MIN_str, self.__date_min))
            self.__set_rule_element_regex_date()
            self.__check_date_correct(value)
        elif key == Rule.DATE_MAX_str:
            self.__date_max = str(value)
            self._logger.debug("%s set with %s" \
                % (Rule.DATE_MAX_str, self.__date_max))
            self.__set_rule_element_regex_date()
            self.__check_date_correct(value)
        elif key == Rule.DATE_FORMAT_str:
            self.__date_format = str(value)
            self._logger.debug("%s set with %s" \
                % (Rule.DATE_FORMAT_str, self.__date_format))
            self.__set_rule_element_regex_date()
            #self.__check_date_format(value)
        elif key == Rule.HIGHLIGHT_FG_NAME:
            self.__highlight_FG = str(value).upper()
            self._logger.debug("%s set with %s" \
                % (Rule.HIGHLIGHT_FG_NAME, self.__highlight_FG))
        elif key == Rule.HIGHLIGHT_BG_NAME:
            self.__highlight_BG = str(value).upper()
            self._logger.debug("%s set with %s" \
                % (Rule.HIGHLIGHT_BG_NAME, self.__highlight_BG))
        elif key == Rule.COLUMNIZE_NAME:
            exec("columnize = dict("
                + str(value) + ")")
            self.__columnize = columnize
            self._logger.debug("%s set with %s" \
                % (Rule.COLUMNIZE_NAME, self.__columnize))
        elif key == Rule.TEMPLATE_NAME:
            self.__template = str(value)
            self._logger.debug("%s set with %s" \
                % (Rule.TEMPLATE_NAME, self.__template))
        elif key == Rule.FUNCTION_NAME:
            #FIXME: FUNCTION_NAME and FUNCTION_TO_EXE
            self.__function[Rule.FUNCTION_NAME] = value
            self._logger.debug("%s set with %s" \
                % (Rule.FUNCTION_NAME, self.__function))
        elif key == Rule.FUNCTION_TO_EXE:
            self.__function[Rule.FUNCTION_NAME] = value
            self._logger.debug("%s set with %s" \
                % (Rule.FUNCTION_TO_EXE, self.__function))
        elif key == Rule.FUNCTION_PATH:
            self.__function[Rule.FUNCTION_PATH] = value
            self._logger.debug("%s set with %s" \
                % (Rule.FUNCTION_PATH, self.__function))
        elif key == Rule.FUNCTION_MODULE:
            self.__function[Rule.FUNCTION_MODULE] = value
            self._logger.debug("%s set with %s" \
                % (Rule.FUNCTION_MODULE, self.__function))
        elif key == Rule.FUNCTION_ARGS_NAME:
            self.__function[Rule.FUNCTION_ARGS_NAME] = value
            self._logger.debug("%s set with %s" \
                % (Rule.FUNCTION_ARGS_NAME, self.__function))
        else:
            self.__rule_ids[key] = value
            self._logger.debug("Rule id %s set with %s" % (key, value))
            self._logger.debug("Rule ids: %s" % self.__rule_ids)

    def __set_rule_element_active(self, value):
        """
        """
        value_lower = value.lower()
        result = None

        if bool(re.match(Rule.ACTIVE_NAMES_pos, value_lower)):
            result = Rule.ACTIVE
        elif bool(re.match(Rule.ACTIVE_NAMES_neg, value_lower)):
            result = Rule.DISABLED

        self.__active = result

        return result

    def __set_rule_element_regex_date(self):
        """
        Checks that the date exists in the regex_str
         as (?P<date>) form.
        """
        result = None
        line   = self.__regex_str

        regex_str = r"\(\?\P\<date\>(.*?)\)"

        if self.__date_regex != None:
            self._logger.debug("Date regex already present: return True")
            return True

        #match_obj = re.search(regex_str, line)
        regex = re.compile(regex_str)
        match_obj = regex.match(line)
        result = bool(match_obj)
        if not(result):
            msg = "The key \"date\" does not exist in the regex.\n" \
                + "Please, check."
            self._logger.error("EXCEPTION RAISED!: " + msg)
            raise Exception(msg)
        else:
            self._logger.debug("The key \"date\" exist in the regex")
            date_regex_str = match_obj.group(1)
            self._logger.debug("The key \"date\" value: %s" % date_regex_str)
            self.__date_regex = re.compile(date_regex_str)

        return result

    def __check_rule_element(self, key, value):
        """
        """
        self._logger.debug("Check Rule elem %s/%s begins" % (key, value))
        #TODO: muchos mas chequeos.
        if key == Rule.ACTIVE_NAME:
            self.__check_rule_element_active(value)
        elif key == Rule.REGEX_NAME:
            self.__check_rule_element_regex(value)
        elif key == Rule.MATCH_SEARCH_NAME:
            self.__check_rule_element_match_search(value)
        elif key == Rule.ACTION_NAME:
            self.__check_rule_element_action(value)
        elif (key == Rule.LINE_AFTER_str) or \
            (key == Rule.LINE_BEFORE_str):
            #
            self.__check_rule_element_line_num(int(value))
        elif (key == Rule.DATE_MIN_str) or \
            (key == Rule.DATE_MAX_str) or \
            (key == Rule.DATE_FORMAT_str):
            #
            self._logger.warning("Check %s to be implemented" % key)
            #FIXME
        elif (key == Rule.HIGHLIGHT_FG_NAME) or \
            (key == Rule.HIGHLIGHT_BG_NAME):
            #
            self._logger.warning("Check %s to be implemented" % key)
            #FIXME
        elif key == Rule.TEMPLATE_NAME:
            self._logger.warning("Check %s to be implemented" % key)
        elif (key == Rule.COLUMNIZE_NAME):
            self._logger.warning("Check %s to be implemented" % key)
            #FIXME
        elif key == Rule.FUNCTION_NAME or \
             key == Rule.FUNCTION_PATH or \
             key == Rule.FUNCTION_MODULE or \
             key == Rule.FUNCTION_ARGS_NAME or \
             key == Rule.FUNCTION_TO_EXE:
            #
            self._logger.warning("Check %s to be implemented" % key)
            #FIXME
        elif key == Rule.REGEX_FLAGS:
            self._logger.warning("Check %s to be implemented" % key)
        else:
            #Check that key exists in regex.
            self.__check_rule_element_id(key)

    def __check_rule_element_active(self, value):
        """
        """
        value  = value.lower()
        result = None

        try:
            result = bool(re.match(Rule.ACTIVE_NAMES, value))
            self._logger.debug("Rule element active checked. OK")
        except Exception, e:
            msg = "The \"active\" value is wrong, please check.\n" \
                + "active: %s \n" % str(value)
            self._logger.error("EXCEPTION RAISED!: " + msg)
            raise Exception(msg)

        return result

    def __check_rule_element_regex(self, value):
        """
        """
        try:
            regex = re.compile(value)
            self._logger.debug("Rule element regex checked. OK")
        except Exception, e:
            msg = "The rule does not contain a valid \
                regular expression.\n" + \
                "regex: %s \n" % value
            self._logger.error("EXCEPTION RAISED!: " + msg)
            raise Exception(msg)

    def __check_rule_element_match_search(self, value):
        """
        """
        regex_str = "%s|%s" % (Rule.MATCH_SEARCH_str1, Rule.MATCH_SEARCH_str2)
        condition = re.match(regex_str, value)
        if not(condition):
            msg = "%s parameter has an abnormal value \"%s\"." \
                % (Rule.MATCH_SEARCH_NAME, str(value))

            self._logger.error("EXCEPTION RAISED!: " + msg)
            raise Exception(msg)

        self._logger.debug("Rule element match search. OK")

    def __check_rule_element_action(self, value):
        """
        """
        value  = value.lower()
        result = None

        try:
            result = bool(re.match(Rule.ACTION_NAMES, value))

        except Exception, e:
            raise Exception("The \"action\" value is wrong, please check.\n" \
                + "action: %s \n" % str(value))

        return result

    def __check_rule_element_id(self, key):
        """
        Checks that the key exists in the regex_str
         as (?P<key>) form.
        """
        #print "__check_rule_element_id: %s" % key

        result = None
        line = self.__regex_str

        regex_str = r"\(\?\P\<%s\>.*\)" % key
        #print regex_str

        # #Check template in all the rule elements
        # rule_elems_dict = dict(self.__rule_elements)
        # template = None
        # if rule_elems_dict.has_key(Rule.TEMPLATE_NAME):
            # template = rule_elems_dict[Rule.TEMPLATE_NAME]

        # if (line is None) and (template is not None):
            # return

        match_obj = re.search(regex_str, line)
        result = bool(match_obj)
        if not(result):
            raise Exception("The key \"%s\" does not exist in the regex.\n" % key \
            + "Please, check." )

        return result

    def __check_rule_element_line_num(self, value):
        """
        """
        if not(isinstance(value, int)):
            raise Exception("Value %s is not valid number. \n" % str(value) + \
                "Please, check.")

        #Check consistency in before and after
        #Check valid numbers (DONE)
        #Check two are present, just before or just after.

    def __check_date_correct(self, value):
        """
        """
        self._logger.debug("Check correct date %s - begins" % str(value))
        date        = value
        date_regex  = self.__date_regex

        try:
            match_obj = date_regex.match(date)
            self._logger.debug("Date regex matches date correctly.")
        except Exception, e:
            string_1 = "date \"%s\" " % str(date)
            string_2 = "date_regex \"%s\" " % str(date_regex)
            string_3 = "don't match"
            #
            msg = string_1 + "and " + string_2 \
                + string_3 + "\n" + str(e)
            self._logger.error("RAISED EXCEPTION!: " + msg)
            raise Exception(msg)

    def __check_date_format(self, value):
        """
        FIXME: DO it!
        """
        date        = value
        factory     = self.__datetime_factory
        format      = self.__date_format

        try:
            factory.strptime(date, format)
        except Exception, e:
            string_1 = "date %s " % str(date)
            string_2 = "format %s " % str(format)
            string_3 = "don't match"
            raise Exception(string_1 + string_2 + string_3 + str(e))

    def __check_at_least_one_rule(self):
        """
        Checks that there is no empty rule, so that no
        inconsistent rules are processed.
        """
        self._logger.debug("Check at least one rule present - begins")
        result = None
        type_of_rule = self.__type_of_rule

        if self.__type_of_rule == Rule.INCLUDEONLY:
            result = (len(self.__include_list) > 0)
        elif self.__type_of_rule == Rule.EXCLUDEONLY:
            result = (len(self.__exclude_list) > 0)
        else:
            #First condition: regex
            condition_1 = bool(self.__regex_str is None)

            #Second condition: line number
            condition_2_1 = bool(self.__line_num_before == Rule.LINE_NUM_BEFORE_MAX)
            condition_2_2 = bool(self.__line_num_after == Rule.LINE_NUM_AFTER_MIN)
            condition_2 = condition_2_1 and condition_2_2

            if condition_1 and condition_2:
                msg = "No condition to analyze was done. Please, check. \n" \
                    + "Rule: %s" % str(self.__regex_str)
                self._logger.error("EXCEPTION RAISED!: " + msg)
                raise Exception(msg)
            else:
                result = True

        self._logger.debug("Check at least one rule result: %s - ends" % str(result))
        return result

    def __set_include_list(self, rule_elements):
        """
        """
        for element in rule_elements:
            key   = element[0]
            value = element[1]
            if key == Rule.ACTIVE_NAME:
                self.__set_rule_element_active(value)
                continue

            self.__include_list.append(element[1])

        self._logger.debug("Includeonly rules set")

    def get_include_list(self):
        """
        """
        self._logger.debug("Include list: %s" % str(self.__include_list))
        return self.__include_list

    def __set_exclude_list(self, rule_elements):
        """
        """
        for element in rule_elements:
            key   = element[0]
            value = element[1]
            if key == Rule.ACTIVE_NAME:
                self.__set_rule_element_active(value)
                continue

            self.__exclude_list.append(element[1])

        self._logger.debug("Excludeonly rules set")

    def get_exclude_list(self):
        """
        """
        self._logger.debug("Exclude list: %s" % str(self.__exclude_list))
        return self.__exclude_list

    def __set_type_of_rule(self):
        """
        Set type of rule depending on the title: INCLUDEONLY_str_1, EXCLUDEONLY_str_1 or STDRULE_str depending on the title value.
        """
        title_lower = self.__title.lower()

        include_only_str = Rule.INCLUDEONLY_re_str
        exclude_only_str = Rule.EXCLUDEONLY_re_str

        #print "title_lower: %s" % title_lower
        if bool(re.match(include_only_str, title_lower)):
            self.__type_of_rule = Rule.INCLUDEONLY
            self._logger.debug("Type of rule set as %s" % Rule.INCLUDEONLY)
        elif bool(re.match(exclude_only_str, title_lower)):
            self.__type_of_rule = Rule.EXCLUDEONLY
            self._logger.debug("Type of rule set as %s" % Rule.EXCLUDEONLY)
        else:
            self.__type_of_rule = Rule.STDRULE_str
            self._logger.debug("Type of rule set as %s" % Rule.STDRULE_str)

    def __del__(self):
        """
        Destructor
        """
        self._logger.verbose("*** class Rule END ***")
