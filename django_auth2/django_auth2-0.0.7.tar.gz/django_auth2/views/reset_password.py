from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth import views as auth_views
from .. import utils
from .. import mails
from .. import forms
from ..tokens import password_reset_token_henerator


class PasswordReset(FormView):
    form_class = forms.PasswordResetForm
    template_name = 'django_auth2/reset_password/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        user = utils.get_user(email=form.cleaned_data['email'])
        mails.send_reset_password_mail(self.request, user)
        return super().form_valid(form)


password_reset = PasswordReset.as_view()

# def password_reset(request, **kwargs):
#     return auth_views.password_reset(request,
#                                      template_name='auth2/reset_password/password_reset_form.html',
#                                      email_template_name='auth2/reset_password/password_reset_email.html',
#                                      **kwargs)


def password_reset_done(request, **kwargs):
    return auth_views.password_reset_done(
        request, template_name='django_auth2/reset_password/password_reset_done.html',
        **kwargs
    )


def password_reset_confirm(request, **kwargs):
    return auth_views.password_reset_confirm(
        request,
        set_password_form=forms.SetPasswordForm,
        token_generator=password_reset_token_henerator,
        template_name='django_auth2/reset_password/password_reset_confirm.html',
        **kwargs
    )


def password_reset_complete(request, **kwargs):
    return auth_views.password_reset_done(
        request,
        template_name='django_auth2/reset_password/password_reset_complete.html',
        **kwargs)
