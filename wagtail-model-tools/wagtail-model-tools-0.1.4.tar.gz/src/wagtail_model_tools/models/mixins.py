from django.db import models
from django.contrib.contenttypes.models import ContentType


__all__ = [
    # Generic mixins
    'CopyMixin',
    'CopyableModel',

    # Page mixins
    'ProxyPageMixin', 'GetAbsoluteUrlPageMixin'
]


class CopyMixin:
    """
    Mixin class that implements a safe .copy() method to create copies of
    model instances even if they are model subclasses.
    """

    def copy(self, overrides=None, commit=True):
        """Return a copy of the object. If commit=False, the copy is not saved
        to the database.

        The optional overrides dictionary defines which attributes should be
        overridden in the copied object.
        """

        # Retrieve data
        data = {
            f.name: getattr(self, f.name)
            for f in self._meta.fields
            if not f.primary_key
        }

        # Save overrides
        if overrides:
            data.update(overrides)

        # Crete object
        new = type(self)(**data)
        if commit:
            new.save()
        return new


class CopyableModel(CopyMixin, models.Model):
    """
    Model that implements a copy() method from CopyMixin.
    """

    class Meta:
        abstract = True


class ProxyPageMixin:
    """
    Page proxy models that saves the proxy content type in the database rather
    than using the parent concrete model.
    """

    def save(self, *args, **kwargs):
        try:
            proxy_ct_id = self.__content_type_id
        except AttributeError:
            cls = type(self)
            proxy_ct = ContentType.objects.get_for_model(cls, False)
            proxy_ct_id = cls.__content_type_id = proxy_ct.id

        if self.content_type_id != proxy_ct_id:
            self.content_type_id = proxy_ct_id

        super().save(*args, **kwargs)


class GetAbsoluteUrlPageMixin:
    """
    Adds a .get_absolute_url() method to the Page instance.
    """

    def get_absolute_url(self):
        return self.url
