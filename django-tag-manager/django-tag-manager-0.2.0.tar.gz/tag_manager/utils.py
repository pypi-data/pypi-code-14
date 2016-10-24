from django.conf import settings
try:
    from django.urls import Resolver404, resolve
except ImportError:
    from django.core.urlresolvers import Resolver404, resolve


def trigger_passes_test(test_func, context):
    return test_func(context['request'], context)


def view_passes_test(view_name, path, **kwargs):
    # Special case for tag included everywhere
    if view_name == '__all__':
        return True

    try:
        view = resolve(path, **kwargs)
        return view_name == view.view_name
    except Resolver404:
        return False


def resolve_tag(context, config=None):
    if config is None:
        config = settings.TAG_MANAGER_CONFIG

    matching_tags = []
    for view_name, tag_config in config.items():
        if isinstance(tag_config, str):
            tag_template, trigger = tag_config, lambda *_, **__: True
        else:
            tag_template, trigger = tag_config

        if view_passes_test(view_name, context['request'].path) \
                and trigger_passes_test(trigger, context):
            matching_tags.append(tag_template)

    return matching_tags
