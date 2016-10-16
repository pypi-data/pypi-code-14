from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from django.urls import reverse


def get_user(**kwargs):
    return get_user_model().objects.get(**kwargs)


def get_user_model():
    if hasattr(settings, 'AUTH_USER_MODEL'):
        app, model = settings.AUTH_USER_MODEL.split('.')
        model = model.lower()
        content_type = ContentType.objects.get(app_label=app, model=model)
        return content_type.model_class()
    else:
        from django.contrib.auth.models import User as DjangoUser
        return DjangoUser


class RedirectActiveUser(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('index'))

        return super(RedirectActiveUser, self).dispatch(request, *args,
                                                        **kwargs)
