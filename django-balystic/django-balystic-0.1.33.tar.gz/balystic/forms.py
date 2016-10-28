from django import forms
from django.forms import widgets


class QAQuestionForm(forms.Form):
    title = forms.CharField(label='title', required=True)
    description = forms.CharField(
        label='description', required=True)
    tags = forms.CharField(
        label='tags', help_text='tags separated by comma',
        required=True)


class QAAnswerForm(forms.Form):
    answer_text = forms.CharField(label='answer', required=True)


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=widgets.PasswordInput)


class SignupForm(forms.Form):
    first_name = forms.CharField(required=False)
    phone_number = forms.CharField(required=False)
    email = forms.EmailField(required=True)
    is_pro = forms.BooleanField(required=False)
    password_1 = forms.CharField(widget=widgets.PasswordInput)
    password_2 = forms.CharField(widget=widgets.PasswordInput)

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        password_1 = cleaned_data.get('password_1', '')
        password_2 = cleaned_data.get('password_2', '')
        if password_1 != password_2 or password_1 == '':
            raise forms.ValidationError(
                'Passwords do not match')


class UpdateUserForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)
    bio = forms.CharField(required=False)
    facebook = forms.URLField(required=False)
    linkedin = forms.URLField(required=False)
    twitter = forms.URLField(required=False)
    isPro = forms.BooleanField(required=False)
