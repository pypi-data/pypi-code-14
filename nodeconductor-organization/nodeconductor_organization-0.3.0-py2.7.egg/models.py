from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from model_utils import FieldTracker

from nodeconductor.core import models as core_models
from nodeconductor.structure.models import Customer, CustomerRole


@python_2_unicode_compatible
class Organization(core_models.UuidMixin,
                   core_models.NameMixin,
                   models.Model):
    abbreviation = models.CharField(unique=True, max_length=8)
    native_name = models.CharField(max_length=160, blank=True, null=True)
    customer = models.OneToOneField(Customer, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '%(name)s (%(abbreviation)s)' % {
            'name': self.name,
            'abbreviation': self.abbreviation
        }


@python_2_unicode_compatible
class OrganizationUser(core_models.UuidMixin, models.Model):
    user = models.OneToOneField(core_models.User)
    is_approved = models.BooleanField(default=False)
    organization = models.ForeignKey(Organization)

    tracker = FieldTracker()

    def __str__(self):
        return '%(username)s | %(abbreviation)s' % {
            'username': self.user.username,
            'abbreviation': self.organization.abbreviation
        }

    def can_be_managed_by(self, user):
        customer = self.organization.customer
        if customer and customer.has_user(user, role_type=CustomerRole.OWNER):
            return True

        return user.is_staff
