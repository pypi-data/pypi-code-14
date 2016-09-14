from django import forms
from django.utils.translation import ugettext_lazy as _

from .constants import (REGULATED_TESTING_CHOICES, REGULATED_ALL, TPA_CHOICES,
    TPA_LAST_MONTH, MRO_LAST_MONTH, MRO_CHOICES, FORM_ACCOUNT_TYPE_CHOICES)


class ReportFilterForm(forms.Form):
    """
    form used for filtering in reports page
    """
    
    account = forms.BooleanField(label=_("Account"), initial=True,
        required=False)
    mro_verification = forms.BooleanField(label=_("MRO Verification"),
        initial=True, required=False)
    date_ccf_matched = forms.BooleanField(label=_("CCF Matched Date"),
        initial=True, required=False)
    date_released = forms.BooleanField(label=_("Date Released"), initial=True,
        required=False)
    account_type = forms.ChoiceField(choices=FORM_ACCOUNT_TYPE_CHOICES,
        required=False)
    regulated_testing = forms.ChoiceField(label=_("Regulated Testing"),
        choices=REGULATED_TESTING_CHOICES, widget=forms.RadioSelect,
        initial=REGULATED_ALL, required=False)
    tpa_reports = forms.ChoiceField(label=_("TPA Reports"), choices=TPA_CHOICES,
        widget=forms.RadioSelect, initial=TPA_LAST_MONTH, required=False)
    mro_reports = forms.ChoiceField(label=_("MRO Reports"), choices=MRO_CHOICES,
        widget=forms.RadioSelect, initial=MRO_LAST_MONTH, required=False)
    filter_name = forms.CharField(max_length=128)
    search_text = forms.CharField(max_length=255, required=False)
    start_date = forms.CharField(max_length=32, widget=forms.HiddenInput)
    end_date = forms.CharField(max_length=32, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(ReportFilterForm, self).__init__(*args, **kwargs)
        counter = 1
        for field in self.fields:
            if field == 'regulated_testing':
                self.fields[field].widget.attrs["class"] = "regulatedTest"
            elif field == 'tpa_reports':
                self.fields[field].widget.attrs["class"] = "tpaReports"
            elif field == 'mro_reports':
                self.fields[field].widget.attrs["class"] = "mroReports"
            elif field == "account_type":
                self.fields[field].widget.attrs["class"] = "form-control accountType"
            elif field == "search_text":
                self.fields[field].widget.attrs["class"] = "text-search form-control"
                self.fields[field].widget.attrs["placeholder"] = _("Search...")
            elif field == "filter_name":
                self.fields[field].widget.attrs["class"] = "filter-name form-control"
                self.fields[field].widget.attrs["placeholder"] = _("Filter name...")
            elif "_date" not in field:
                self.fields[field].widget.attrs["class"] = "toggle-column"
                self.fields[field].widget.attrs["data-column"] = counter
                counter += 1
