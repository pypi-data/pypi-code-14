from string import maketrans, punctuation, whitespace
from traceback import format_exc


"""
If I've done things properly, this whole file and the concept of formatters can go away.
but it can't yet.
I think.
"""


class Formatter(object):
    """ Formatting operations for syntax objects

    Name functions after the property they will be operating on.
    All function should take one argument of 'property'.
    """

    @classmethod
    def apply(cls, syntax_obj):
        """ Apply all formatters to the given object 
        
        This method will search the given syntax object for any property which
        has the same name as a formatter.

        Args:
            syntax_obj (object): The object with the attributes to be formatted
        """
        for prop_name, value in list(syntax_obj.__dict__.items()):
            try:
                formatter = getattr(cls, prop_name)

                setattr(syntax_obj, prop_name, formatter(value))
            except AttributeError:
                pass
            except Exception as e:
                print(format_exc())
                print(e)
                print(syntax_obj, '->', prop_name)


class NameFormatter(Formatter):
    """ Base Formatter for object names like variables/functions/classes """

    @classmethod
    def code(cls, property):
        if property:
            filter = maketrans(whitespace, ''.join(['_' for x in whitespace]))
            property = property.translate(filter)
        return property


class CallableFormatter(NameFormatter):
    """ This formatter should be used on callable objects like decorators and fuctions """

    @classmethod
    def name(cls, property):
        """ Replace all punctuation in a callables name with underscores """
        property = super(CallableFormatter, cls).code(property)
        filter = maketrans(punctuation, ''.join(['_' for x in punctuation]))
        return property.translate(filter)

    @classmethod
    def arg_names(cls, property):
        """ Abstract function for formatting positional arguments """
        return property

    @classmethod
    def kwarg_pairs(cls, property):
        """ Abstract function for formatting keyword arguments """
        return property


class CallFormatter(CallableFormatter):
    """ The formatter that should be used when calling functions """

    @classmethod
    def arg_names(cls, property):
        """ Quote data in positional arguments so that it will be passed into a call """
        return property


class QuotedFormatter(Formatter):
    """ Quotes the objects code in 'single quotes' """

    @classmethod
    def code(cls, property):
        return "'"+property+"'"

