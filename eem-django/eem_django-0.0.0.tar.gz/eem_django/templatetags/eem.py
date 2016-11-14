from django.conf import settings
from django.template import Library
from eem_py.url import signed_url

register = Library()


@register.simple_tag
def eem_image(source, **kwargs):
    return signed_url(
        settings.EEM_KEY,
        settings.EEM_HOST,
        source,
        debug=getattr(settings, 'EEM_DEBUG', False),
        **kwargs
    )
