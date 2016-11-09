from django.conf.urls import url
from . import views

app_name = 'django_sabayon'

urlpatterns = [
    url(r'^\.well-known/acme-challenge/(?P<acme_token>\w+)$',
    views.acme_challenge)
]
