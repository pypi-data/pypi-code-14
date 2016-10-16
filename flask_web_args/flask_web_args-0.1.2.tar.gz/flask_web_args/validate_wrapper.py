import inspect

from flask import request
from functools import wraps

import validator

error_handler_func = None


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
            assert isinstance(arg_type, validator.Validator), "default params must be Validator instances but is {}".format(type(arg_type))

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
