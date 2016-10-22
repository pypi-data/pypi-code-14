from django.utils.translation import get_language

from cms.settings.models import Settings


def current_lang():
    # Alias for get_language.
    return get_language()


def served_langs():
    return ('any', get_language())


def generate_meta(title=None, title_suffix=True, description=None,
                  robots=None):
    try:
        settings = Settings.objects.get(language=current_lang())
    except Settings.DoesNotExist:
        settings = Settings.objects.get(language__in=served_langs())

    if title_suffix is None:
        title_suffix = settings.page_title_site_name_suffix
    if title_suffix:
        if title:
            title += ' {} '.format(settings.suffix_separator)
        title += settings.site_name
    if not title:
        title = settings.site_name
    print(title)
    return {
        'title': title,
        'description': description or settings.meta_description,
        'robots': robots or settings.meta_robots
    }
