from django.contrib import auth
from django.shortcuts import redirect, render
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
        user.is_active = False
        user.save()
        mails.send_activation_mail(self.request, user)

        # user_cache = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password2'])
        #
        # auth.login(self.request, user_cache)
        return render(self.request, template_name='django_auth2/register/email_sended.html')

register = Register.as_view()
