from django.db import models
from django.utils.translation import ugettext_lazy as _

from feincms import extensions


class Extension(extensions.Extension):

    def handle_model(self):

        # Add custom fields to the (Page) class
        self.model.add_to_class(
            'search_exclude',
            models.BooleanField(
                verbose_name=_('Search exclude'),
                help_text=("Exclude page from search indexing"),
                default=False))

    def handle_modeladmin(self, modeladmin):
        # Add custom fields to the admin class
        modeladmin.add_extension_options(_('Search'), {
            'fields': ['search_exclude', ],
        })
