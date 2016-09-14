from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^filters/remove/(?P<pk>.*\d+)/$', views.RemoveFilter.as_view(),
        name="delete-filter"),
    url(r'^reports-average/(?P<average_type>.*\w+)/$',
        views.DashboardAverage.as_view(), name="reports-average"),
    url(r'^reports-released/$', views.ReportsReleased.as_view(),
        name="reports-released"),
    url(r'^reports-export/(?P<export_type>csv|pdf)/$',
        views.ExportReports.as_view(), name="reports-export"),
    url(r'^reports-ajax/$', views.ReportListAjax.as_view(), name="reports-ajax"),
    url(r'^reports/$', views.ReportList.as_view(), name="reports"),
    url(r'^top-accounts/$', views.TopAccounts.as_view(), name="top-accounts"),
    url(r'^users/$', views.UsersList.as_view(), name="accounts"),
    url(r'^$', views.Dashboard.as_view(), name="index"),
]
