# coding=utf-8
from __future__ import unicode_literals
from django import forms

from formed import settings as formed_settings
from form_elements import page_elements_from_definition, form_field_from_definition


class DefinitionFormBase(forms.Form):
    form_definition = None
    form_definition_page = None

    store_in_session = False  # Should the data of this form be stored in the session?

    error_css_class = formed_settings.FORMED_FORM_ERROR_CSS_CLASS
    required_css_class = formed_settings.FORMED_FORM_REQUIRED_CSS_CLASS
    label_suffix = formed_settings.FORMED_FORM_LABEL_SUFFIX

    def __init__(self, form_definition, form_definition_page=0,
                 form_definition_page_type=formed_settings.FORM_DEFINITION_PAGE_TYPE_PAGE, **kwargs):
        """
        Initializes a Form using the given form definition
        :param formed.models.FormDefinition form_definition:
        :param int form_definition_page:
        :param str form_definition_page_type:
        :param kwargs:
        :return:
        """
        if 'data' in kwargs and formed_settings.FORM_DEFINITION_PAGE_TYPE_FIELD in kwargs['data']:
            # Copy because we can't mutate request.POST:
            kwargs['data'] = kwargs['data'].copy()
            # Force the page type (don't use POST'ed value):
            kwargs['data'][formed_settings.FORM_DEFINITION_PAGE_TYPE_FIELD] = form_definition_page_type

        super(DefinitionFormBase, self).__init__(**kwargs)

        self.form_definition = form_definition
        self.form_definition_page = form_definition_page

        self.fields[formed_settings.FORM_DEFINITION_ID_FIELD] = forms.IntegerField(
            widget=forms.HiddenInput,
            initial=form_definition.pk
        )
        self.fields[formed_settings.FORM_DEFINITION_PAGE_FIELD] = forms.IntegerField(
            widget=forms.HiddenInput,
            initial=self.form_definition_page
        )
        self.fields[formed_settings.FORM_DEFINITION_PAGE_TYPE_FIELD] = forms.CharField(
            widget=forms.HiddenInput,
            initial=form_definition_page_type
        )
        # setattr(self, 'clean_form_definition_page_type', lambda: self.clean_form_definition_page_type)

    def clean_form_definition_page_type(self):
        # todo: since the name of this field is dynamic (FORM_DEFINITION_PAGE_TYPE_FIELD) so should this clean_* method.
        value = self.cleaned_data[formed_settings.FORM_DEFINITION_PAGE_TYPE_FIELD]
        if value not in formed_settings.FORM_DEFINITION_PAGE_TYPES:
            raise forms.ValidationError("Value should be one of '{}'.".format("', '".join(
                formed_settings.FORM_DEFINITION_PAGE_TYPES
            )))
        return value

    def get_previous_page(self):
        return None

    def get_next_page(self):
        """
        There is no next form page
        :return:
        """
        return None

    def pages(self):
        """
        Returns a list of pages in the current form definition
        :return:
        """
        pages = []
        for page_index in range(self.form_definition.page_count()):
            pages.append(page_elements_from_definition(self.form_definition, page_index, self))
        return pages


class DefinitionPageForm(DefinitionFormBase):
    store_in_session = True

    def __init__(self, **kwargs):
        """
        Initializes a Form using the given form definition page
        :param kwargs:
        :return:
        """
        super(DefinitionPageForm, self).__init__(**kwargs)

        for field in self.form_definition.fields(page_index=self.form_definition_page):
            name, form_field = form_field_from_definition(field)
            self.fields[name] = form_field

    def has_previous_page(self):
        return self.form_definition.has_previous_page(self.form_definition_page)

    def has_next_page(self):
        return self.form_definition.has_next_page(self.form_definition_page)

    def get_previous_page(self):
        return self.form_definition.get_previous_page(data=self.cleaned_data, current_page=self.form_definition_page)

    def get_next_page(self):
        return self.form_definition.get_next_page(data=self.cleaned_data, current_page=self.form_definition_page)

    def page(self):
        """
        Returns a list of fieldsets in the current page.
        :rtype: list
        """
        return page_elements_from_definition(self.form_definition, self.form_definition_page, self)

    def fieldsets(self):
        """
        Alias for the page() method
        :return:
        """
        return self.page()


class DefinitionSummaryForm(DefinitionFormBase):
    """
    A form for the summary page. Mostly used for the hidden inputs of the current form definition.
    Could also be used to ask the user if he wants a confirmation mail?
    """

    def __init__(self, **kwargs):
        super(DefinitionSummaryForm, self).__init__(
            form_definition_page_type=formed_settings.FORM_DEFINITION_PAGE_TYPE_SUMMARY,
            **kwargs
        )

    def get_previous_page(self):
        """
        The 'current' page is the last page of the form, go back to that page.
        :return:
        """
        return self.form_definition_page

    def clean_form_definition_page_type(self):
        return formed_settings.FORM_DEFINITION_PAGE_TYPE_SUMMARY


class DefinitionFinishForm(DefinitionFormBase):
    """
    A form for the finish view. Not sure if we need this though.
    No going back or forwards from here
    """

    def __init__(self, **kwargs):
        super(DefinitionFinishForm, self).__init__(
            form_definition_page_type=formed_settings.FORM_DEFINITION_PAGE_TYPE_FINISH,
            **kwargs
        )

    def clean_form_definition_page_type(self):
        return formed_settings.FORM_DEFINITION_PAGE_TYPE_FINISH
