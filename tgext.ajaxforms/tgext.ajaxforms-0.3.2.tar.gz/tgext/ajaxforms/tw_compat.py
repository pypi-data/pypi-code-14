try:
    from tw.api import JSLink as Tw1JSLink, Link as Tw1Link, JSSource as Tw1JSSource
    class TW1:
        JSLink = Tw1JSLink
        Link = Tw1Link

        jquery_js = Tw1JSLink(modname=__name__, filename='statics/jquery.min.js')
        jquery_form_js = Tw1JSLink(modname=__name__, filename='statics/jquery.form.js')
        ajaxforms_js = Tw1JSSource(location='head', src='''
    var tgext_ajaxforms = tgext_ajaxforms || {};
    tgext_ajaxforms.jQuery = jQuery.noConflict(true);
''')
        spinner_icon = Tw1Link(modname=__name__, filename='statics/spinner.gif')
except ImportError:
    class TW1:
        pass

try:
    from tw2.core.resources import JSLink as Tw2JSLink, Link as Tw2Link, JSSource as Tw2JSSource
    class TW2:
        JSLink = Tw2JSLink
        Link = Tw2Link

        jquery_js = Tw2JSLink(modname=__name__, filename='statics/jquery.min.js')
        jquery_form_js = Tw2JSLink(modname=__name__, filename='statics/jquery.form.js')
        ajaxforms_js = Tw2JSSource(location='head', src='''
    var tgext_ajaxforms = tgext_ajaxforms || {};
    tgext_ajaxforms.jQuery = jQuery.noConflict(true);
''')
        spinner_icon = Tw2Link(modname=__name__, filename='statics/spinner.gif')
except ImportError:
    class TW2:
        pass

def is_tw2_form(w):
    return hasattr(w, 'req')

def inject_widget_resources(w):
    if is_tw2_form(w):
        resources = [r.req() for r in w.resources]
        for r in resources:
            r.prepare()

        for c in w.children_deep():
            #Some widgets modify the resources during prepare
            c = c.req()
            c.prepare()

            resources = [r.req() for r in c.resources]
            for r in resources:
                r.prepare()
    else:
        w.register_resources()

def form_class_name(w):
    if is_tw2_form(w):
        return w.__name__
    else:
        return w.__class__.__name__