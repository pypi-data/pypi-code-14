from django.dispatch import Signal, receiver
from model_reference.utils import normalize_name as _normalize_name


#: A signal that is triggered when the user tries to load an empty reference.
#: Handlers may construct the reference object before raising an error. The
#: resulting object is registered and returned.
empty_reference_signal = Signal(providing_args=['name'])


class ProtectedError(Exception):
    """
    Raised when registering duplicate references.
    """


class EmptyReferenceError(Exception):
    """
    Raised when a trying to load an object from a non-existing reference.
    """


class InvalidReferenceError(Exception):
    """
    Raised when reference points to an invalid object.
    """


def register(instance, name=None, *, suffix=None, protect=False, silent=False):
    """
    Register a reference to the given object under the given name or suffix.

    Args:
        instance:
            Any saved instance of a Django model.
        name:
            String used to reference the given object.
        suffix:
            If the user specify a suffix rather than a name, the name is
            constructed as 'app_label.model:suffix'. This is useful to avoid
            collisions with references from different models.
        protect:
            Prevents registering a new object on an existing reference. Raises
            a ProtectedError if a different object is already registered for the
            given reference.
        silent:
            If True, and protect is also True, prevents the ProtectError from
            being raised.

    Returns:
        A Reference instance.
    """

    from model_reference.models import Reference

    return Reference.objects.register(instance, name,
                                      suffix=suffix,
                                      protect=protect,
                                      silent=silent)


def load(name, model=None, factory=None):
    """
    Load the instance registered using the given name. If model is also given,
    construct the reference name as 'app_label.model:name'.

    Args:
        name:
            Reference name or suffix.
        model:
            If given, interpret the first argument as a suffix and extract the
            app_label and model name from the Model subclass.
        factory:
            A factory function which is called if the given reference do not
            exist to construct the appropriate referred object. The resulting
            reference is automatically saved on the database.
    """

    from model_reference.models import Reference

    return Reference.objects.load(name, model=model, factory=factory)


def factory(name, model=None):
    """
    Register a factory function for creating objects for an empty reference of
    the given name. If model is given, name is treated as a suffix.

    Usage:

        @factory('favorite_beatle')
        def make_beatle():
            john, created = User.objects.get_or_create(
                username='john',
                email='john@apple.com'
            )
            return john

    If a reference to 'favorite_beatle' does not exist in the database, it will
    be automatically created by the make_beatle function if one calls
    load('favorite_beatle').
    """

    from django.db.models import Model
    from model_reference.models import Reference
    real_name = _normalize_name(name, model)

    def decorator(func):
        @receiver(empty_reference_signal)
        def handler(name, **kwargs):
            if real_name == name:
                obj = func()
                if not isinstance(obj, Model):
                    raise TypeError('expect a Model instance, got: %r' % obj)
                return obj
        func.handler = handler
        return func

    return decorator
