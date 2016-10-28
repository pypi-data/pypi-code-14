# -*- coding: utf-8 -*-
# Created by Gustavo Del Negro <gustavodelnegro@gmail.com> on 9/30/16.
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from translation_server.models import *


class TranslationAdminForm(forms.ModelForm):
    languages_list = [lang[0].replace('-', '_') for lang in settings.LANGUAGES]

    def clean(self):
        cleaned_data = super(TranslationAdminForm, self).clean()

        for language in self.languages_list:
            if cleaned_data.get("text_"+language) == cleaned_data.get('auxiliary_text_'+language):
                self.add_error('auxiliary_text_' + language,
                               forms.ValidationError(_('DTSE1')))

        return cleaned_data

    def save(self, commit=False):
        translation = super(TranslationAdminForm, self).save(commit=commit)
        translation.save()
        translation.migration_created = False
        translation.save()
        return translation

    class Meta:
        model = Translation
        fields = "__all__"


class TranslationTypeAdminForm(forms.ModelForm):
    class Meta:
        model = TranslationType
        fields = "__all__"