import codecs
import sys

from bs4 import UnicodeDammit

from pyramid.tweens import INGRESS

PY3 = sys.version_info[0] == 3


def unicodedammit_tween_factory(handler, registry):

    def unicodedammit_tween(request):
        env = request.environ
        qs = env.get('QUERY_STRING', '')

        if qs:
            try:
                if PY3:
                    # Use latin-1 to handle PEP-3333 "native string" definition
                    qs = codecs.encode(qs, 'latin-1')
                codecs.utf_8_decode(qs, 'strict', True)
            except UnicodeDecodeError:
                ud = UnicodeDammit(qs)
                if PY3:
                    env['QUERY_STRING'] = codecs.decode(
                        codecs.encode(ud.unicode_markup, 'utf-8'), 'latin-1',
                    )
                else:
                    env['QUERY_STRING'] = codecs.encode(ud.unicode_markup,
                                                        'utf-8')

        return handler(request)

    return unicodedammit_tween


def includeme(config):
    config.add_tween('pyramid_unicodedammit.unicodedammit_tween_factory',
                     under=INGRESS)
