from django.conf.urls import url, include

urlpatterns = [
    url(r'^health/', include('django_site_health.urls')),
]

