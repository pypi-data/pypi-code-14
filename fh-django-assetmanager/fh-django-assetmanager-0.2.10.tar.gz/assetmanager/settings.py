from django.conf import settings

STORAGE = getattr(settings, 'ASSETMANAGER_STORAGE', None)
PAGE_SIZE = getattr(settings, 'ASSETMANAGER_PAGE_SIZE', 10)
IMAGE_CONTENT_TYPES = getattr(settings, 'ASSETMANAGER_IMAGE_CONTENT_TYPES',
                              ('image/jpeg', 'image/png', 'image/gif',
                               'image/svg+xml'))

PREVIEW_URL_TEMPLATE = getattr(settings, 'ASSETMANAGER_PREVIEW_URL_TEMPLATE', None)