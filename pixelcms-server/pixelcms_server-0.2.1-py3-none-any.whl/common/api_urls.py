from django.conf.urls import url, include

from cms.router import urls as router_urls
from cms.nav import urls as nav_urls
from cms.content import urls as content_urls
from cms.accounts import urls as accounts_urls
from cms.emails import urls as emails_urls
from cms.live_admin import urls as live_admin_urls


urlpatterns = [
    url(r'^route/', include(router_urls)),
    url(r'^nav/', include(nav_urls)),
    url(r'^content/', include(content_urls)),
    url(r'^accounts/', include(accounts_urls)),
    url(r'^emails/', include(emails_urls)),
    url(r'^live-admin/', include(live_admin_urls))
]
