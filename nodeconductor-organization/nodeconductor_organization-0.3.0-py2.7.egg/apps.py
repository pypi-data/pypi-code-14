from __future__ import unicode_literals

from django.apps import AppConfig
from django.db.models import signals

from nodeconductor_organization import handlers


class OrganizationConfig(AppConfig):
    name = 'nodeconductor_organization'
    verbose_name = "NodeConductor Organization"

    # See, https://docs.djangoproject.com/en/1.7/ref/applications/#django.apps.AppConfig.ready
    def ready(self):
        OrganizationUser = self.get_model('OrganizationUser')

        signals.post_save.connect(
            handlers.log_organization_user_save,
            sender=OrganizationUser,
            dispatch_uid='nodeconductor_organization.handlers.log_organization_user_save',
        )

        signals.post_delete.connect(
            handlers.log_organization_user_delete,
            sender=OrganizationUser,
            dispatch_uid='nodeconductor_organization.handlers.log_organization_user_delete',
        )
