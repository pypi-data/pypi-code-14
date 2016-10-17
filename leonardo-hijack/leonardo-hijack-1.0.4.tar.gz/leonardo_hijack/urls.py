
from django.conf.urls import include, url

urlpatterns = [
    url(r'^hijack/', include('hijack.urls')),
]
