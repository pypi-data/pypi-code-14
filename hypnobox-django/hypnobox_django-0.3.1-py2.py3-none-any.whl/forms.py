# coding: utf-8
from __future__ import unicode_literals

from django import forms

from .models import Lead


class LeadForm(forms.ModelForm):

    class Meta:
        model = Lead
        fields = (
            'name', 'email', 'phone_prefix', 'phone_number',
            'product_id', 'media',
        )
        widgets = {
            'product_id': forms.HiddenInput(),
            'media': forms.HiddenInput(),
        }
