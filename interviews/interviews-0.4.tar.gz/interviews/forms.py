from django import forms

from .models import Picture


class FilterPictureForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FilterPictureForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            qs = Picture.objects.filter(interview=kwargs['instance'].interview)
            self.fields['related_pictures'].queryset = qs
