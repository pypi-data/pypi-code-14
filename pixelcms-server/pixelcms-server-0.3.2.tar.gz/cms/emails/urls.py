from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^contact-form/$',
        views.ContactFormView.as_view()
    )
]
