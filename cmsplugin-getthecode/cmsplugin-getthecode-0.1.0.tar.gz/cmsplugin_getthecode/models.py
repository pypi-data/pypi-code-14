####################################################################################################

from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin
from filer.fields.image import FilerFileField

from pygments.styles import get_all_styles
from pygments.lexers import get_all_lexers

####################################################################################################

class SourceCodeFile(CMSPlugin):

    """
    A django CMS Plugin to use source code
    """

    STYLE_CHOICES = [(x, x) for x in get_all_styles()]
    LANGUAGE_CHOICES = [(x, x) for x in sorted([x[1][0] for x in get_all_lexers()])]

    # cmsplugin_ptr = models.OneToOneField(
    #     CMSPlugin,
    #     related_name='+',
    #     parent_link=True,
    # )

    source_file = FilerFileField(
        verbose_name=_('file'),
        null=True,
        on_delete=models.SET_NULL,
    )

    code_language = models.CharField(
        verbose_name=_('code language'),
        max_length=20,
        choices=LANGUAGE_CHOICES,
    )

    style = models.CharField(
        verbose_name=_('style'),
        max_length=255,
        choices=STYLE_CHOICES,
        default='default',
    )

    line_numbers = models.BooleanField(
        verbose_name=_('line numbers'),
        default=False
    )

    ##############################################

    def __str__(self):

        """ Instance's name shown in structure page """

        return "Source Code {}" .format(self.source_file.name)
