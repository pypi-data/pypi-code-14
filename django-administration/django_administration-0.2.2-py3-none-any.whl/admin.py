from django.contrib.admin import ModelAdmin


class ListDisplayMixin(object):
    """
    Extends ``list_display` syntax for default ``ModelAdmin``.

    Usage:
        class MyAdmin(ModelAdmin):
            list_display = (
                # [...]
                ('field', field_formatter),
            )
    """
    list_display = ()

    def __init__(self, model, admin_site):
        # For re-assignment, list_display should be mutable
        self.list_display = list(self.list_display)

        for i, attr_name in enumerate(self.list_display):
            if isinstance(attr_name, tuple):
                attr_name, filter_func = attr_name[0], attr_name[1]
                new_attr_name = '_%s' % attr_name

                # Replace tuple elements with string one, so it's invisible to parent class
                self.list_display[i] = new_attr_name

                def closure(attr_name, filter_func):
                    def func(admin_cls, instance):
                        return filter_func(admin_cls, instance, getattr(instance, attr_name), attr_name)
                    return func

                # Keep original references in closure
                new_filter_func = closure(attr_name, filter_func)

                # Provides a convenient column name (verbose_name or default)
                field = model._meta.get_field(attr_name)
                new_filter_func.short_description = getattr(field, 'verbose_name', attr_name)

                # Attach custom method to class
                setattr(self.__class__, new_attr_name, new_filter_func)

        super(ListDisplayMixin, self).__init__(model, admin_site)


class LabelMixin(object):
    """
    Provides Bootstrap ``label`` CSS for Django admin.

    See: http://getbootstrap.com/components/#labels
    """
    class Media:
        css = {
            'all': ('administration/css/label.css',)
        }


class ModelAdmin(LabelMixin, ListDisplayMixin, ModelAdmin):
    pass
