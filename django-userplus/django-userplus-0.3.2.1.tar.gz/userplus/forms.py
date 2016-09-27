import re

from django import forms
from django.contrib.auth import get_user_model
from django.conf import settings


class SignUpForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        kwargs = {'set_activation_key': getattr(settings, 'USERPLUS_SET_ACTIVATION_KEY')}
        user.is_active = not kwargs['set_activation_key']
        if commit:
            user.save(**kwargs)
        return user


class SignInForm(forms.Form):
    username_or_email = forms.CharField(
        label='Enter your username or email', max_length=70)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_username_or_email(self):
        user_id = self.cleaned_data.pop('username_or_email')

        if re.match(r"[^@]+@[^@]+\.[^@]+", user_id):
            self.cleaned_data['email'] = user_id
        else:
            self.cleaned_data['username'] = user_id


class FacebookSigninForm(forms.Form):
    access_token = forms.CharField(required=True)


class FormWithFacebook(object):
    def __init__(self, other_form, data=None):
        self.facebook_form = FacebookSigninForm(data)
        self.other_form = other_form(data)

    def is_valid(self):
        return self.facebook_form.is_valid() or self.other_form.is_valid()

    def get_valid_form(self):
        if self.facebook_form.is_valid():
            self.valid_form_is_facebook = True
            return self.facebook_form
        elif self.other_form.is_valid():
            return self.other_form
