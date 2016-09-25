from __future__ import unicode_literals

from nodeconductor.structure.log import event_logger


def log_organization_user_save(sender, instance, created=False, **kwargs):
    if created:
        event_logger.user_organization.info(
            'User {affected_user_username} has claimed organization {affected_organization}.',
            event_type='user_organization_claimed',
            event_context={
                'affected_user': instance.user,
                'affected_organization': instance.organization.abbreviation,
            })
    else:
        previously_approved = instance.tracker.previous('is_approved')
        currently_approved = instance.is_approved
        if not previously_approved and currently_approved:
            event_logger.user_organization.info(
                'User {affected_user_username} has been approved for organization {affected_organization}.',
                event_type='user_organization_approved',
                event_context={
                    'affected_user': instance.user,
                    'affected_organization': instance.organization.abbreviation,
                })
        elif previously_approved and not currently_approved:
            event_logger.user_organization.info(
                'User {affected_user_username} claim for organization {affected_organization} has been rejected.',
                event_type='user_organization_rejected',
                event_context={
                    'affected_user': instance.user,
                    'affected_organization': instance.organization.abbreviation,
                })


def log_organization_user_delete(sender, instance, **kwargs):
    event_logger.user_organization.info(
        'User {affected_user_username} has been removed from organization {affected_organization}.',
        event_type='user_organization_removed',
        event_context={
            'affected_user': instance.user,
            'affected_organization': instance.organization.abbreviation,
        })
