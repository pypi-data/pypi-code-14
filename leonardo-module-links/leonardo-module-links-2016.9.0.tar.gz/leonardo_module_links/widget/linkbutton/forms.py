
from django.utils.translation import ugettext_lazy as _
from leonardo.forms.fields.dynamic import DynamicModelChoiceField
from leonardo.module.web.widgets.forms import WidgetUpdateForm
from leonardo_module_links.models import Link


class LinkWidgetForm(WidgetUpdateForm):

    link = DynamicModelChoiceField(
        label=_("Link"),
        help_text=_("Select a link."),
        queryset=Link.objects.all(),
        search_fields=[
            'web_address__icontains',
        ],
        cls_name='leonardo_module_links.link',
        form_cls='leonardo_module_links.forms.LinkForm')
