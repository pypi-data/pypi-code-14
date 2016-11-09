
class ReadOnlyAdminPreMixin(object):
    change_form_template = 'ievv_djangoadmin/ievv_djangoadmin_mixins/' \
                           'read_only_change_form.django.html'
    actions = None

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.get_fields()]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, id=None):
        return False
