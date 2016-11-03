"""
Module that make validations depnding on parameters.

This module uses several classes to make different types of
validations.
"""
import logging

class Validation:
    """
    Father class for all the validations.

    Class that contain the constructor of the object and have
    the father callable method.

    Subclasses need to override the method _validation.
    """
    def __init__(self, lamb, name):
        if callable(lamb):
            self.lamb = lamb
        else:
            raise TypeError("lamb should be a lambda")
        if type(name) == str:
            self.name = name
        else:
            raise TypeError("name should be a string")


    def __call__(self, received, typefn):
        return self._validationstructure(self.name, received, typefn, self.lamb)


    def _valudationalgorithm(self, name, received, typefn, validatecasted):
            pass


    def _validationstructure(self, name, received, typefn, validatecasted):
        try:
            return self._valudationalgorithm(name, received, typefn, validatecasted)
        except (ValueError, TypeError) as e:
            logging.warning(self._errorMessage(name, str(e)))
            return self._errorMessage(name)


    def _errorMessage(self, name, exception=''):
        return (('%s: %s was invalid', str(exception), name) if exception 
                    else ('%s was invalid' % name))



class Multivalue(Validation):
    """
    Class for the Multivalue validation.

    This class implements the Validation class, it
    override the _validation method with the local
    method _multivalued.
    """
    def _valudationalgorithm(self, name, received, typefn, validatecasted):
        values = received.split(',')
        casted = [typefn(value) for value in values]
        return '' if validatecasted(casted) else (self._errorMessage(name))


class MultivalueAll(Multivalue):
    """
    Class for the Multivalue_all validation.

    This class implements the Multivalue class
    and overrides the _validation method with thefather 
    method _multivalued using the local method _typeorall.
    """
    def __call__(self, received, typefn):
        return self._validationstructure(self.name, received, self._typeorall(typefn), self.lamb)


    def _typeorall(self, fn):
        def callback(value):
            if value == 'all':
                return value
            else:
                return fn(value)
        return callback


class Univalue(Validation):
    """
    Class for the Univalue validation.

    This class implements the Validation class, it
    override the _validation method with the local
    method _valued.
    """
    def _valudationalgorithm(self, name, received, typefn, validatecasted):
        if type(received) == typefn:
            return '' if validatecasted(received) else (self._errorMessage(name))
        else:
            raise TypeError


class UnivaluePosType(Validation):
    """
    Class for the Univalue_pos_type validation.

    This class implements the Validation class, it
    override the _validation method with the local
    method _typed.
    """
    def __init__(self, name):
        self.lamb = lambda x:True
        if type(name) == str:
            self.name = name
        else:
            raise TypeError("name should be a string")

    def _valudationalgorithm(self, name, received, typefn, lamb):
        typefn(received)
        if typefn is int and int(received) < 0:
            raise ValueError(name + ' cannot be negative')
        return ''


def validate_keys(schema, params):
    return list(set(schema.keys()) - set(params.keys()))


def validate(schema, params):
    """
    Function that validates a schema with parameters
    
    Validates each entry of params against the cooresponding entry of the
    schema using functions in this file.
    """
    errors = {}
    missing = validate_keys(schema, params)

    if len(missing) > 0:
        mistrs = ''
        for k in missing[:-1]:
            mistrs += str(k) + ', '
        mistrs += str(missing[len(missing) - 1])
        logging.warning('There is/are %d missing keys: %s.',
                        len(missing), mistrs)
        errors['missing'] = missing

    for key, validator in schema.iteritems():
        if key not in params:
            continue
        error = validator(params[key][0], params[key][1])
        errors.update({key: error} if error else {})

    logging.warning('There were %d errors.', len(errors))
    return errors

