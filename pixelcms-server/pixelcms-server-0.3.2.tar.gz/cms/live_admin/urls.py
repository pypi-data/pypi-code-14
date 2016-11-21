from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^editable-content/$',
        views.EditableContentView.as_view()
    )
]
