"""
http://docs.wagtail.io/en/v1.6.3/reference/hooks.html#editor-interface`
"""
from django.utils.html import format_html, format_html_join
from django.conf import settings
from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.whitelist import attribute_rule, check_url

def whitelister_element_rules():
    return {
        'a': attribute_rule({'href': check_url, 'target': True}),
        'blockquote': attribute_rule({'class': True}),
    }
hooks.register('construct_whitelister_element_rules', whitelister_element_rules)

def editor_js():
    js_files = [
        'wagtail_hallo_plugins/wagtail_hallo_plugins.js',
    ]
    js_includes = format_html_join('\n', '<script src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files)
    )

    html = "<script>"
    if 'superscript' in settings.WAGTAIL_HALLO_PLUGINS:
        html += "registerHalloPlugin('superscriptbutton');"
    if 'subscript' in settings.WAGTAIL_HALLO_PLUGINS:
        html += "registerHalloPlugin('subscriptbutton');"
    html += "</script>"
    print(html)

    return js_includes + format_html(html)

hooks.register('insert_editor_js', editor_js)

def editor_css():
    return format_html('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css">')

hooks.register('insert_editor_css', editor_css)
