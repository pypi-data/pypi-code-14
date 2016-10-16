import ast
import inspect
import logging

from flask import request
from functools import wraps

error_handler_func = None


def _parse_param_to_list(arg_name, arg_value):
    """
    Return a list from a string list
    Values we can parse as list
        1. A string of the format ['a', 'b']
        2. A comma separated string a,b,c
    :param arg_value: e.g. "['a', 'b']"
    :return:
        error: error_msg, []
        success: "", result_list
    """
    if "[" in arg_value:
        try:
            return "", map(str, ast.literal_eval(arg_value))  # [] case
        except ValueError:
            msg = "{} {} is not of the for \"['x', 'y']\"".format(arg_name, arg_value)
            return msg, []
    return "", map(str, arg_value.split(","))  # , case


def _validate_kwargs(kwargs_passed, kwargs_types):
    """
    Validate all the arguments passed
    :param kwargs_passed: {arg_name: arg_value}
    :param kwargs_types: {arg_name: Validator}
    :return:
        error: arg_name, arg_value, error_msg
        success: "", "", ""
    """
    for kwarg_name, kwarg_value in kwargs_passed.iteritems():
        kwarg_type = kwargs_types[kwarg_name]

        error_msg, validated_arg_value = kwarg_type._parse_arg(kwarg_name, kwarg_value)

        if error_msg:
            return kwarg_name, kwarg_value, error_msg

        kwargs_passed[kwarg_name] = validated_arg_value

    return "", "", ""


def validate_args(func):

    # View function needs to be unique so we need to over write the name of the function to match the calling function
    @wraps(func)
    def func_wrapper(**kwargs):
        # Get the function param and default values
        args_inspect = inspect.getargspec(func)
        arg_names = args_inspect.args
        arg_types = args_inspect.defaults
        if len(arg_names) == 0:  # No required or optional parameters are expected
            return func()

        assert len(arg_names) == len(arg_types), "All args must have a type"
        for arg_type in arg_types:
            assert isinstance(arg_type, Validator), "default params must be Validator instances but is {}".format(type(arg_type))

        kwargs_types = dict(zip(arg_names, arg_types))

        optional_params_passed = set(request.args.keys())

        # Be defensive. If a parameter has the same key as one of the 'required' params drop it
        # e.g. /api/<foo> and the url passed is /api/1?foo=10. We want to drop foo=10
        required_params_passed = set(kwargs.keys())
        optional_params_passed = optional_params_passed - required_params_passed

        # remove any parameters that we don't recognize/expect. so the union of the expected and passed parameters
        optional_params_passed = optional_params_passed & set(arg_names)

        # At this point we have the valid optional params that where passed for every parameter passed in function
        # We need to go through all the kwarg names and make sure that they are populate properly
        for arg_name in arg_names:
            if arg_name in required_params_passed:  # This was a url passed required parameter
                assert kwargs_types[arg_name].required is not False, "{} is part of url and is required. It can't be optional".format(arg_name)
                kwargs_types[arg_name].required = True
                continue
            elif arg_name in optional_params_passed:  # This was a passed argument in the url
                kwargs[arg_name] = request.args.get(arg_name)
            else:
                # The value wasn't required and wan't passed so we need to set it to None
                kwargs[arg_name] = None

        # Validate all the kwargs are of the right type
        arg_name, arg_value, error_msg = _validate_kwargs(kwargs, kwargs_types)

        if error_msg:
            return error_handler_func(arg_name, arg_value, error_msg)

        return func(**kwargs)

    return func_wrapper


class Validator:

    VALID_TYPES = [str, unicode, int, float, long, bool, list]

    def __init__(self, arg_type=None, valid=None, default=None, valid_value=None, required=None):
        """
        :param arg_type: The expected type. arg_type needs to be in VALID_TYPES. Is inferred from default if default is passed
        :param valid: A list of valid values or a func(value) which will return True if valid, false otherwise
        :param default: The default value if None is passed. Will be used to infer the arg_type. Cannot be passed with required=True
        :param valid_value: Returns the value to use or None if value is invalid. Cannot be used with valid at the same time
        :param required: If true and the argument must be passed and must be valid. url param args are automatically required.
        """
        # Validate that we have a valid callbackfunction
        assert error_handler_func is not None, "You have to declare a callback function for error_handling"
        assert callable(error_handler_func), "The error handler function must be a function of type func(arg_name, arg_value, error_msg)"

        assert arg_type is None or type(arg_type) == type, "arg_type must be of type"
        self.arg_type = arg_type

        assert valid is None or callable(valid) or type(valid) is list, "valid must be function/lambda or a list"
        if type(valid) is list:
            valid = map(str, valid)  # Make sure to cast everything to a string to avoid later processing
        self.valid = valid

        self.default = default
        # We need to make sure that the if default and valid are passed, that default is valid
        error_msg = self._check_value_is_valid("__unknown__", default)
        assert error_msg == "", error_msg
        # If we don't pass in a valid_value then we have to pass one of either arg_type or default
        assert valid_value or (bool(arg_type) != bool(default)), "arg_type can be inferred from default so don't pass both"
        if default is not None:
            assert type(default) in Validator.VALID_TYPES, "default needs to be one of of type {}".format(Validator.VALID_TYPES)
            self.arg_type = type(default)

        assert valid_value is None or callable(valid_value), "valid_value must be a function/lambda"
        self.valid_value = valid_value

        assert required is None or type(required) is bool
        assert (not required) or (required and default is None), "You can't pass default when required"
        self.required = required

        # We need one of those two values
        assert self.arg_type != bool(valid_value), "one of arg_type/default or valid_value have to be not None"
        xor_of_valid = bool(valid) != bool(valid_value)
        assert (valid is None and valid_value is None) or xor_of_valid, "at most one of valid and valid_value should be passed"

    def _parse_arg(self, name, value):
        """
        Validate if that value is valid based on the Validator instance criteria
        :param name: the argument name
        :param value: the value of the argument
        :return:
            error: error_msg, None
            success: "", parsed_value
        """
        error_msg = ""

        if value is None:
            if self.required:
                error_msg = "{} cannot be empty".format(name)
                return error_msg, None

            if self.default:
                return "", self.default

            return "", None

        if self.valid_value:
            parsed_value = self.valid_value(value)
            if parsed_value is None:
                error_msg = "{} {} is not valid".format(name, value)
            elif self.arg_type is not None and self.arg_type is not type(parsed_value):
                logging.warning("arg_type is {} but valid_value returned {}. They should match"
                            .format(self.arg_type, type(parsed_value)))
            return error_msg, parsed_value

        assert value is not None and self.valid_value is None and error_msg == "" and self.arg_type is not None

        if self.arg_type is list:  # Parsing to a list requires special processing
            error_msg, parsed_value = _parse_param_to_list(name, value)
            if error_msg:
                return error_msg, parsed_value
        else:
            try:
                parsed_value = self.arg_type(value)
            except (TypeError, ValueError):
                error_msg = "{} {} is not of type {}".format(name, value, self.arg_type)
                return error_msg, None

        assert parsed_value is not None and error_msg == ""

        error_msg = self._check_value_is_valid(name, parsed_value)
        if error_msg:
            return error_msg, None

        return "", parsed_value

    def _check_value_is_valid(self, name, value):
        """
        Using the self.valid validate if the value is valid
        :param name: the argument name
        :param value: the value of the argument
        :return:
            error: error_msg
            success: ""
        """
        error_msg = ""

        if value is None or self.valid is None:
            return error_msg

        if callable(self.valid):  # function/lambda
            is_valid = self.valid(value)
            assert is_valid is True or is_valid is False, "valid func(value) must return True of False"
            if not is_valid:
                error_msg = "{} {} is not valid".format(name, value)
        else:  # is a list
            assert type(self.valid) is list
            # A. if value is a list then check that is is a subset of valid
            # B. else just check that it is in valid
            if type(value) is list:
                diff_list = set(value) - set(self.valid)
                if len(diff_list) != 0:  # We have an invalid value in the list
                    error_msg = "{} list {} has invalid value(s) of {}. Valid options are {}".format(
                        name, value, list(diff_list), self.valid)
            else:
                if value not in self.valid:
                    error_msg = "{} {} is not in {}".format(name, value, self.valid)

        return error_msg
