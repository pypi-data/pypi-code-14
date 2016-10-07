# coding: utf-8
from django.contrib import auth
from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView

from ..utils import RedirectActiveUser
from ..forms import LoginForm


class Login(RedirectActiveUser, FormView):
    form_class = LoginForm
    template_name = 'django_auth2/login/login.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return super(Login, self).form_valid(form)

login = Login.as_view()
