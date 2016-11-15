from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


def duplicate(self, request, queryset):
    for q in queryset:
        try:
            q.pk = None
            q.save()
        except:
            self.message_user(
                request,
                _('Failed to duplicate "{}".').format(q),
                level=messages.ERROR
            )
duplicate.short_description = _('Duplicate selected items')
