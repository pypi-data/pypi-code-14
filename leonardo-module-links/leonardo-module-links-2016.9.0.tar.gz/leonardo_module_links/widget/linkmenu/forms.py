

from django.utils.translation import ugettext_lazy as _
from leonardo.forms.fields.dynamic import DynamicModelChoiceField
from leonardo.module.web.widgets.forms import WidgetUpdateForm
from leonardo_module_links.models import LinkCategory


class LinksWidgetForm(WidgetUpdateForm):

    list = DynamicModelChoiceField(
        label=_("Links"),
        help_text=_("Select a list of links."),
        queryset=LinkCategory.objects.all(),
        search_fields=[
            'name__icontains',
            'slug__icontains',
            'description__icontains',
        ],
        cls_name='leonardo_module_links.linkcategory',
        form_cls='leonardo_module_links.forms.LinksForm')
