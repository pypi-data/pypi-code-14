from django.db.models.manager import ManagerDescriptor
from django.contrib.contenttypes.models import ContentType
from wagtail.wagtailcore.models import Page, PageManager
from .mixins import GetAbsoluteUrlPageMixin

__all__ = ['SinglePage', 'SinglePageMixin', 'SinglePageManager']

SECOND_INSTANCE_ERROR = (
    'Trying to create a second instance of %(cls)s\n'
    'Please do not try to create or instantiate %(cls)s objects '
    'explicitly. Instead, use the %(cls)s.objects.instance() '
    'interface.'
)


class MixinManagerDescriptor:
    """
    Descriptor to a manager that is suitable to be present in MixinClasses.

    Django does not behave well when managers are defined in mixin classes that
    do not inherit from Model. This fixes this.
    """
    def __init__(self, manager_class, name='objects'):
        self.manager_class = manager_class
        self.name = name

    def __get__(self, instance, type=None):
        if instance is not None:
            raise AttributeError("Manager isn't accessible via %s instances" %
                                 type.__name__)

        manager = self.manager_class()
        manager.name = self.name
        manager.model = type
        descriptor = ManagerDescriptor(manager)
        setattr(type, self.name, descriptor)
        return descriptor.__get__(None, type)


class SinglePageManager(PageManager):
    """
    A PageManager with the .instance() method to retrieve the single instance
    object.
    """

    def instance(self):
        """
        Return the single instance for the SingleModel.
        """

        return self.model.instance()


class SinglePageMixin(GetAbsoluteUrlPageMixin):
    """
    The mixin version of SimplePage.
    """

    __instance_id = None
    objects = MixinManagerDescriptor(SinglePageManager)

    @classmethod
    def instance(cls):
        """
        Return the single instance.
        """

        if cls.__instance_id is not None:
            # The __instance_id cache fails in test environments since the
            # database is rolled back after each test and the cached id will
            # most likely become invalid. If this cached check fails, we
            # proceed normally
            try:
                return cls.objects.get(id=cls.__instance_id)
            except cls.DoesNotExist:
                pass

        try:
            content_type = get_content_type(cls)
            instance = cls.objects.get(content_type=content_type).specific
        except cls.DoesNotExist:
            instance = object.__new__(cls)
            state = instance.get_state()
            instance.__init__(**state)
            parent = instance.get_parent()
            parent.add_child(instance=instance)

        cls.__instance_id = instance.id
        return instance

    def get_parent(self):
        """
        Return the parent page instance.
        """

        return Page.objects.get(path='00010001')

    def get_state(self):
        """
        Return a dictionary with the instance state. The state dictionary must
        provide initialization data such as the page title, slug, seo_title,
        etc.

        Must be overridden in subclasses.
        """

        raise NotImplementedError(
            'SinglePage subclasses must override the .get_state() method. It '
            'must return a dictionary that is passed as kwargs of a newly '
            'created instance.'
        )

    def save(self, *args, **kwargs):
        instance_id = self.__instance_id
        if self.id is None:
            cls = self.__class__
            try:
                content_type = get_content_type(cls)
                cls.objects.get(content_type=content_type)
            except cls.DoesNotExist:
                pass
            else:
                name = self.__class__.__name__
                raise ValueError(SECOND_INSTANCE_ERROR % {'cls': name})

        super().save(*args, **kwargs)
        self.__instance_id = self.id


class SinglePage(SinglePageMixin, Page):
    """
    A page subclass that has a single entry in the database.

    This implementation do not prevent the page object from being instantiated
    several times. Instead, all instances must point to the same entry in the
    database.

    Subclasses should implement the ``cls.get_state()`` and (optionally) the
    ``cls.get_parent()`` methods. These are used to create single instances
    when no instance is fhould oin the database.
    """

    class Meta:
        abstract = True

    objects = SinglePageManager()


def get_content_type(cls):
    return ContentType.objects.get_for_model(cls, for_concrete_model=False)
