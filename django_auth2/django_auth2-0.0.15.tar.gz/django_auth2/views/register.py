from django.conf import settings
from django.contrib import auth
from django.shortcuts import render, redirect
from django.views.generic import FormView
from ..forms import RegisterForm
from .. import utils
from .. import mails
from ..utils import RedirectActiveUser


class Register(RedirectActiveUser, FormView):
    form_class = RegisterForm
    template_name = "django_auth2/register/register.html"

    def form_valid(self, form):
        form.save()

        user = utils.get_user(username=form.cleaned_data['username'])

        if getattr(settings, 'DJANGO_AUTH2_SEND_ACTIVATION_EMAIL', False):
            user.is_active = False
            mails.send_activation_mail(self.request, user)
            return render(
                self.request, template_name='django_auth2/register/email_sended.html'
            )
        else:
            user.is_active = True
            user.save()

            username_name_field = utils.get_user_model().USERNAME_FIELD
            user_kwargs = {username_name_field: getattr(user, username_name_field)}
            user_cache = auth.authenticate(
                password=form.cleaned_data['password1'], **user_kwargs)

            if user_cache is not None:
                auth.login(self.request, user_cache)
                return redirect('index')

register = Register.as_view()
