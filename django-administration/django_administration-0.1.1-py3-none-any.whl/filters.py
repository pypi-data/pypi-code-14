from django.contrib.admin.filters import AllValuesFieldListFilter, RelatedFieldListFilter


class DropdownFilter(AllValuesFieldListFilter):
    template = 'administration/dropdown_filter.html'


class RelatedDropdownFilter(RelatedFieldListFilter):
    template = 'administration/dropdown_filter.html'
