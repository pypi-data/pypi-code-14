from functools import lru_cache

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.query import ModelIterable

from model_reference import empty_reference_signal, EmptyReferenceError, \
    ProtectedError, InvalidReferenceError
from model_reference.utils import normalize_name


class ReferenceManager(models.Manager):
    """
    Specialized manager for the Reference model.
    """

    def load(self, name, model=None, factory=None):
        """
        Load reference from the database.

        Same as the :func:`model_reference.load` function.
        """

        # Load reference
        normalized_name = normalize_name(name, model)
        try:
            ref = self.get(name=normalized_name)
        except self.model.DoesNotExist:
            pass
        else:
            return ref.load()

        # Create instance from factory function
        if factory is not None:
            instance = factory()

        # Create instance from empty_reference_signal handlers
        else:
            trigger = empty_reference_signal.send
            responses = trigger(self.model, name=normalized_name)
            responses = {
                (res.pk, type(res)): res
                for func, res in responses if res is not None
            }

            if len(responses) == 1:
                instance, = responses.values()
            elif len(responses) == 0:
                raise EmptyReferenceError(
                    'No object were found for %r reference' % normalized_name
                )
            else:
                raise RuntimeError(
                    'Multiple handlers were registered for empty %r '
                    'references' % normalized_name
                )

        # Register newly created instance and return
        self.register(instance, normalized_name)
        return instance

    def register(self, instance, name=None, *,
                 suffix=None, protect=False, silent=False):
        """
        Create reference from the given model instance.

        Same as the :func:`model_reference.register` function.
        """

        # Normalize reference name
        cls = type(instance)
        if name is None and suffix:
            name = normalize_name(name, cls)
        elif name is None:
            name = normalize_name(name, cls)[:-1]

        # Fetch attributes
        app_label = cls._meta.app_label
        model = cls._meta.model_name
        instance_pk = instance.pk

        # Create object
        ref, created = self.get_or_create(
            name=name,
            app_label=app_label,
            model=model,
            instance_pk=instance_pk
        )

        # Check protection
        if not created and protect:
            if not (ref.instance_pk == instance_pk and
                            ref.app_label == app_label and
                            ref.model == model):
                if silent:
                    return
                else:
                    raise ProtectedError(
                        'A reference to %r is already registered' % name
                    )

        # Update object if it was not created
        elif not created:
            if (ref.instance_pk != instance_pk or
                        ref.app_label != app_label or
                        ref.model != model):
                ref.app_label = app_label
                ref.model = model
                ref.instance_pk = instance_pk
                ref.save()
        return ref


class ReferenceQuerySet(models.QuerySet):
    """
    Specialized queryset for the Reference model.
    """

    def instance(self, silent=False):
        """
        Convert reference to an instance.
        """
        reference = self.get()
        return reference.load(silent)

    def instances(self, silent=False):
        """
        Convert all references in the queryset to instances.
        """

        clone = self._clone()
        clone._iterable_class = InstanceIterable
        clone._silent_invalid_reference_errors = silent
        return clone


class InstanceIterable(ModelIterable):
    """
    Iterates over objects referred by Reference instances.
    """

    def __iter__(self):
        silent = self.queryset._silent_invalid_refernce_errors
        for obj in super().__iter__():
            yield obj.load(silent=silent)


class Reference(models.Model):
    """
    Store named references to model instances.
    """

    name = models.CharField(max_length=140, unique=True)
    instance_pk = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    objects = ReferenceManager.from_queryset(ReferenceQuerySet)()

    def load(self, silent=False):
        """
        Load instance from reference.

        Raises an InvalidReferenceError if reference is invalid. If silent=True,
        return None for invalid references.
        """

        try:
            cls = get_type(self.app_label, self.model)
            return cls.objects.get(pk=self.instance_pk)
        except (TypeError, ObjectDoesNotExist):
            if silent:
                return None
            raise InvalidReferenceError(
                'Reference %s.%s:%s points to an invalid object' %
                (self.app_label, self.model, self.instance_pk)
            )


@lru_cache(maxsize=256)
def get_type(app_label, model):
    """
    Return type from app_label and model name.
    """

    try:
        content_type = ContentType.objects.get(app_label=app_label, model=model)
        return content_type.model_class()
    except ContentType.DoesNotExist:
        raise TypeError('invalid type: %s.%s' % (app_label, model))