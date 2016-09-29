# coding=utf-8
import collections
import copy
import json
from operator import itemgetter

from django.conf import settings
from django.contrib import admin
from django.contrib.admin import RelatedFieldListFilter
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from formed import settings as formed_settings
from formed.models import FormDefinition, FormSubmission, FormSubmissionNotification


def update_deep(d, u):
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            r = update_deep(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


def dict_merge(dct, merge_dct):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.
    :param dct: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: None
    """
    for k, v in merge_dct.items():
        if k in dct and isinstance(dct[k], dict) and isinstance(merge_dct[k], dict):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]


class RelatedOnlyFieldListFilter(RelatedFieldListFilter):
    """
    This filter is added to Django 1.8 by default, since we support 1.6 we add it here
    """

    def field_choices(self, field, request, model_admin):
        limit_choices_to = {'pk__in': set(model_admin.get_queryset(request).values_list(field.name, flat=True))}
        return field.get_choices(include_blank=False, limit_choices_to=limit_choices_to)


class SortedRelatedOnlyFieldListFilter(RelatedOnlyFieldListFilter):
    """
    Extends RelatedOnlyFieldListFilter and simply sorting the resulting choices by their name.
    """

    def field_choices(self, field, request, model_admin):
        choices = super(SortedRelatedOnlyFieldListFilter, self).field_choices(field, request, model_admin)
        by_name = itemgetter(1)
        return sorted(choices, key=by_name)


class FormSubmissionNotificationInlineFormSet(BaseInlineFormSet):
    def clean(self):
        """
        Validate the FormSubmissionNotifications and check if there is at least one that is not sent as a copy.
        :return:
        """
        super(FormSubmissionNotificationInlineFormSet, self).clean()
        forms = []
        for form in self.forms:
            # Filter out empty forms
            cleaned = form.clean()
            if cleaned:
                forms.append(cleaned)

        if forms:
            has_non_copy = False
            for cleaned in forms:
                if not cleaned['DELETE'] and 'copy' in cleaned and cleaned['copy'] is None:
                    has_non_copy = True
                    break
            if not has_non_copy:
                raise ValidationError(
                    _('At least one notification should NOT be sent as a copy (CC or BCC).'),
                    code='no-non-copy'
                )


class FormSubmissionNotificationInline(admin.TabularInline):
    model = FormSubmissionNotification
    formset = FormSubmissionNotificationInlineFormSet
    min_num = 0
    extra = 1


class FormDefinitionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created', 'modified',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created', 'modified',)
    fieldsets = (
        (None, {
            'fields': [
                ('name', 'slug',),
            ]
        }),
        (_('Form definition'), {
            'fields': [
                'definition',
            ]
        }),
        (_('After submitting the form...'), {
            'fields': [
                'enable_summary',
                'finish_title',
                'finish_text',
            ]
        }),
        (_('Confirmation E-mail'), {
            'fields': [
                'send_confirmation_email',
                'confirmation_email_show_summary',
                'confirmation_email_subject',
                'confirmation_email_text',
            ]
        }),
        (_('Notification E-mail'), {
            'fields': [
                'notification_email_subject',
            ]
        }),
    )
    inlines = (FormSubmissionNotificationInline,)

    class Media:
        css = {
            'all': (
                'admin/form_definition/css/formed.css',
            )
        }
        js = (
            # 'http://cdnjs.cloudflare.com/ajax/libs/vue/1.0.15/vue.min.js',
            'admin/form_definition/js/vendor/vue-1.0.15.js',
            'admin/form_definition/js/vendor/Sortable-1.4.2.min.js',
            'admin/form_definition/js/form-definition-field.js',
        )

    # generic view add/change implementation (used by following add/change/changeform function)
    def view_content(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}

        form_fields_json = {}
        # Merge categories with form fields
        for category, fields in formed_settings.FORMED_FORM_FIELD_CATEGORIES.items():
            for field_name in fields:
                if category not in form_fields_json:
                    form_fields_json[category] = []

                form_field = copy.deepcopy(formed_settings.FORMED_FORM_FIELD)
                field = copy.deepcopy(formed_settings.FORMED_FORM_FIELDS.get(field_name))
                dict_merge(form_field, field)
                form_fields_json[category].append(form_field)

        extra_context['form_fields_json'] = mark_safe(json.dumps(form_fields_json))
        extra_context['formed_show_json_field'] = formed_settings.FORMED_SHOW_JSON_FIELD

        return {'request': request, 'object_id': object_id, 'form_url': form_url, 'extra_context': extra_context}

    # wrapper function specific for django 1.6 Backward compatibility
    def add_view(self, request, form_url='', extra_context=None):
        result = self.view_content(request, form_url=form_url, extra_context=extra_context)
        return super(FormDefinitionAdmin, self).add_view(result['request'], result['form_url'], result['extra_context'])

    # wrapper function specific for django 1.6 Backward compatibility
    def change_view(self, request, object_id=None, form_url='', extra_context=None):
        result = self.view_content(request, object_id=object_id, form_url=form_url, extra_context=extra_context)
        return super(FormDefinitionAdmin, self).change_view(result['request'], result['object_id'], result['form_url'],
                                                            result['extra_context'])

    # default function (1.7 and up)
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        result = self.view_content(request, object_id=object_id, form_url=form_url, extra_context=extra_context)
        return super(FormDefinitionAdmin, self).changeform_view(result['request'], result['object_id'],
                                                                result['form_url'], result['extra_context'])


class FormSubmissionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'form_definition', 'source', 'get_first_full_name', 'created',)
    list_filter = [
        ('form_definition', SortedRelatedOnlyFieldListFilter),
        'created',
    ]

    readonly_fields = ('form_definition', 'source', 'source_url', 'created', 'modified',)
    fieldsets = (
        (None, {
            'fields': (
                'form_definition',
                'source',
                'source_url',
                ('created', 'modified',)
            )
        }),
    )

    def get_list_filter(self, request):
        """
        Returns the available list filters with respect to the Django 'sites' framework.
        :param request:
        :return:
        """
        list_filter = super(FormSubmissionAdmin, self).get_list_filter(request)

        if 'django.contrib.sites' in settings.INSTALLED_APPS:
            list_filter.append('form_definition__sites')

        return list_filter


admin.site.register(FormDefinition, FormDefinitionAdmin)
admin.site.register(FormSubmission, FormSubmissionAdmin)
