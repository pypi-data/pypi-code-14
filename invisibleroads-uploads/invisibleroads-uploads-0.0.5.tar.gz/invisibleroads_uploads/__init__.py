from invisibleroads_macros.iterable import set_default

from .views import add_routes


def includeme(config):
    configure_settings(config)
    configure_assets(config)
    add_routes(config)


def configure_settings(config):
    settings = config.registry.settings
    set_default(settings, 'uploads.tokens.length', 32, int)
    settings['website.dependencies'].append(config.package_name)


def configure_assets(config):
    config.add_cached_static_view(
        '_/invisibleroads-uploads', 'invisibleroads-uploads:assets')
