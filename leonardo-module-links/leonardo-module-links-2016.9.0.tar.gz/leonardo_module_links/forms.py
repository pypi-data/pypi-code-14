
import copy

from crispy_forms.bootstrap import *
from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.layout import *
from crispy_forms.layout import HTML, Layout
from django import forms
from django.forms.models import modelformset_factory
from django.utils.translation import ugettext_lazy as _
from horizon_contrib.forms import SelfHandlingModelForm
from horizon_contrib.forms.models import create_or_update_and_get
from leonardo.forms.fields.dynamic import DynamicModelChoiceField
from leonardo.module.media.fields import ImageField
from leonardo_module_links.models import Link, LinkCategory


class LinkForm(SelfHandlingModelForm):

    id = forms.IntegerField('id', widget=forms.widgets.HiddenInput)
    image = ImageField(required=False)

#    relationship = ModelChoiceField(
#        label=_("Relationship"),
#        help_text=_("Select a link."),
#        queryset=Link.objects.all(),
#        search_fields=[
#            'web_address__icontains',
#        ])

    def __init__(self, *args, **kwargs):
        super(LinkForm, self).__init__(*args, **kwargs)

#        self.init_layout()

#    tabs = {
#        'base': {
#            'name': _('Base'),
#            'fields': (
#                'id', 'name', 'description',
#                'image', we
#                )
#        }
#    }
#        self.helper.layout = Layout(
#            TabHolder(
#                Tab(_('Base'),
#                    'id', 'name', 'description'
#                    ),
#            )
#        )

    class Meta:
        model = Link
        exclude = tuple()

LinkFormset = modelformset_factory(
    Link, form=LinkForm, can_delete=True, extra=1)


class LinksForm(SelfHandlingModelForm):

    id = forms.IntegerField(
        'id', widget=forms.widgets.HiddenInput, required=False)

    form_size = 'lg'

    def __init__(self, *args, **kwargs):
        super(LinksForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            TabHolder(
                Tab(_('Base'),
                    'id', 'name', 'slug', 'description',
                    ),
            )
        )
        if 'request' in kwargs:
            from .tables import LinksTable
            _request = copy.copy(kwargs['request'])
            _request.POST = {}
            _request.method = 'GET'

            try:
                category = self._meta.model.objects.get(
                    id=kwargs['initial']['id'])
            except:
                category = None
                data = []
            else:
                data = category.link_set.all()

            dimensions = Tab(_('Links'),
                             HTML(
                                 LinksTable(_request,
                                            category=category,
                                            data=data).render()),
                             )
            self.helper.layout[0].append(dimensions)

    def handle_related_models(self, request, obj):
        """Handle related models
        """
        formset = LinkFormset(
            request.POST, prefix='links')

        if formset.is_valid():
            for form in formset:
                data = form.cleaned_data
                data.pop('DELETE', None)
                data['category'] = obj
                link = Link(**data)
                link.save()
        else:
            for form in formset.forms:
                if form.is_valid():
                    if 'id' in form.cleaned_data:
                        form.cleaned_data['category'] = obj
                        form.save()
                else:
                    # little ugly
                    data = form.cleaned_data
                    data['category'] = obj
                    raise Exception(data)
                    if 'id' in data and isinstance(data['id'], Link):
                        data['id'] = data['id'].id
                    data.pop('DELETE', None)
                    create_or_update_and_get(Link, data)

        # optionaly delete dimensions
        if formset.is_valid():
            formset.save(commit=False)
            # delete objects
            for obj in formset.deleted_objects:
                obj.delete()
        return True

    class Meta:
        model = LinkCategory
        exclude = tuple()
