####################################################################################################

from django.utils.translation import ugettext_lazy as _

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from pygments import highlight, styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from .models import SourceCodeFile

####################################################################################################

class GetTheCodePlugin(CMSPluginBase):

    model = SourceCodeFile
    name = _('Source Code File')
    render_template = "cmsplugin_getthecode/plugin.html"

    # Editor fieldsets
    # fieldsets = (
    #     (None, {
    #         'fields': (
    #             'source_file',
    #             'code_language',
    #             'style',
    #             'line_numbers',
    #         ),
    #     })
    # )

    ##############################################

    def render(self, context, instance, placeholder):

        # print(instance.source_file.url, )

        source_file = instance.source_file
        source = ''
        with open(source_file.path) as f:
            source = f.read()

        style = styles.get_style_by_name(instance.style)
        formatter = HtmlFormatter(linenos=instance.line_numbers, style=style)
        html = highlight(source, get_lexer_by_name(instance.code_language), formatter)
        css = formatter.get_style_defs()

        context.update({'source_html': html,
                        'css': css,
                        'source_file': source_file,
                        'placeholder': placeholder})
        return context

####################################################################################################

plugin_pool.register_plugin(GetTheCodePlugin)
