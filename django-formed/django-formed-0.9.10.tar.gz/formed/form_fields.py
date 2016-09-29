# coding=utf-8
from django import forms


class TextareaField(forms.CharField):
    widget = forms.Textarea


class SelectField(forms.CharField):
    widget = forms.Select


class RadioField(forms.CharField):
    widget = forms.RadioSelect


class CheckboxField(forms.CharField):
    widget = forms.CheckboxInput


class MultipleChoiceCheckboxField(forms.MultipleChoiceField):
    widget = forms.CheckboxSelectMultiple


class FirstNameField(forms.CharField):
    """
    A custom name field which is used to extract the senders name from the form fields
    """


class LastNamePrefixField(forms.CharField):
    """
    A custom name field which is used to extract the senders name from the form fields
    """


class LastNameField(forms.CharField):
    """
    A custom name field which is used to extract the senders name from the form fields
    """


class NameField(forms.CharField):
    """
    A custom name field which is used to extract the senders name from the form fields
    """


class ConfirmationEmailField(forms.EmailField):
    """
    A normal EmailField which is used to mark a field as the recipient for the confirmation E-mail.
    """


class PhoneField(forms.CharField):
    """
    A field specifically for phone numbers
    """
