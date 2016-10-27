"""cubicweb-ckeditor application package

WYSIWYG js editor with ckeditor
"""

from logilab.common.decorators import monkeypatch, cached

from cubicweb.web.webconfig import WebConfiguration
from cubicweb.web.request import _CubicWebRequestBase


@monkeypatch(_CubicWebRequestBase)
@cached  # so it's writed only once
def fckeditor_config(self):
    ckeditor_url = self.uiprops.get(
        'CKEDITOR_URL',
        '//cdn.ckeditor.com/4.5.7/standard/ckeditor.js')
    self.add_js(ckeditor_url, localfile=False)
    self.add_js('initwysiwyg.js')
    # we should wait CKEDITOR to be loaded before trying to use it
    self.add_onload('''
      var buildWysiwygEditorsInterval = setInterval(function() {
        if (typeof CKEDITOR != "undefined") {
          buildWysiwygEditors();
          clearInterval(buildWysiwygEditorsInterval);
        } else {
          console.log('waiting for CKEDITOR to be loaded');
        }
      }, 200);
    ''')
    base_path = self.uiprops.get('CKEDITOR_BASEPATH')
    if base_path:
        self.html_headers.define_var('CKEDITOR_BASEPATH', base_path)
    self.html_headers.define_var('cklang', self.lang)
    self.html_headers.define_var('ckconfigpath',
                                 self.data_url('ckeditor-config.js'))

@monkeypatch(WebConfiguration)
def fckeditor_installed(self):
    if self.uiprops is None:
        return False
    return True


@monkeypatch(WebConfiguration)
def cwproperty_definitions(self):
    for key, pdef in super(WebConfiguration, self).cwproperty_definitions():
        yield key, pdef
