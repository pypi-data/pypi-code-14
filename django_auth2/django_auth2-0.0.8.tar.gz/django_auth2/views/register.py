from django.conf import settings
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

        if hasattr(settings, 'SEND_ACTIVATION_EMAIL') and settings.SEND_ACTIVATION_EMAIL:
            user.is_active = False
            mails.send_activation_mail(self.request, user)
            return render(
                self.request, template_name='django_auth2/register/email_sended.html'
            )
        else:
            user.is_active = True
            user.save()
            return redirect('index')

register = Register.as_view()
