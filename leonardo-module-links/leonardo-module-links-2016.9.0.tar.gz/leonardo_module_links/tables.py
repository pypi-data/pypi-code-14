
from django.utils.translation import ugettext_lazy as _
from horizon import tables
from horizon.tables.formset import FormsetDataTable, FormsetRow
from leonardo_module_links.models import Link
from .forms import LinkFormset


class CustomFormsetRow(FormsetRow):

    def __init__(self, column, datum, category):
        self.category = category
        super(CustomFormsetRow, self).__init__(column, datum, category)
        # add initial
        if not datum and column.data:
            try:
                previous = column.data[0]
                self.category.fields['id'].initial = previous.id + 1
            except Exception:
                pass


class LinksTable(FormsetDataTable):

    formset_class = LinkFormset

    def get_formset(self):
        """Provide the formset corresponding to this DataTable.

        Use this to validate the formset and to get the submitted data back.
        """
        if self.category:
            queryset = self.category.link_set.all()
        else:
            queryset = Link.objects.none()
        if self._formset is None:
            self._formset = self.formset_class(
                self.request.POST or None,
                initial=self._get_formset_data(),
                prefix=self._meta.name,
                queryset=queryset)
        return self._formset

    def __init__(self, *args, **kwargs):
        self._meta.row_class = CustomFormsetRow
        self.category = kwargs.pop('category', None)
        super(LinksTable, self).__init__(*args, **kwargs)

    id = tables.Column('id', hidden=True)
    category = tables.Column('category', hidden=True)
    web_address = tables.Column('web_address', verbose_name=_("Link"))
    target = tables.Column('target', verbose_name=_('Target'))
    relationship = tables.Column(
        'relationship', verbose_name=_('Relationship'))
    image = tables.Column('image', verbose_name=_('Image'))
    visible = tables.Column('visible',
                            verbose_name=_('Visible'))
    ordering = tables.Column('ordering', verbose_name=_('Ordering'))

    name = 'links'

    class Meta:
        name = 'links'
        table_name = 'Links'
