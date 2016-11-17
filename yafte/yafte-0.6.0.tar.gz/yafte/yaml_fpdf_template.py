# YamlFPDFTemplate
#
# Allows to define a template in yaml
from fpdf import FPDF
import yaml


def rgb(col):
    return (col // 65536), (col // 256 % 256), (col % 256)


class MissingParameterError(Exception):

    def __init__(self, param, *args, **kwargs):
        super().__init__('element {0} configuration incorrect'.format(
            param), *args, **kwargs)
    pass


class YaFTe():

    def __init__(self, filename):

        with open(filename, 'r') as f:
            self.tconfig = yaml.load(f.read())
        self.tconfig.pop('templates', {})
        self.elements = {}
        self.pdf = FPDF(**self.get_fpdfoptions(), unit="mm")
        self.set_docoptions()
        self.prepare_elements()
        self.pdf.set_auto_page_break(False)

    def get_fpdfoptions(self):
        options = {}
        try:
            options['format'] = self.tconfig['docoptions'].pop('format', 'A4')
            options['orientation'] = self.tconfig[
                'docoptions'].pop('orientation', 'portrait')
        except:
            MissingParameterError('docoptions')
        return options

    def add_page(self, **kwargs):
        self.pdf.add_page()
        for key, element in sorted(
                self.elements.items(), key=lambda x: x[1]['priority']):
            current_element = element.copy()
            if key in kwargs:
                current_element['text'] = kwargs[key]
            self.add_to_page(current_element)
        pass

    def add_to_page(self, element):
        try:
            type = element.pop('type', 'unknown')
            getattr(self, 'element_{0}'.format(type))(**element, type=type)
        except Exception as e:
            print(e)
            pass

    def output(self, *args, **kwargs):
        return self.pdf.output(*args, **kwargs)

    def set_docoptions(self):
        for key, value in self.tconfig.pop('docoptions', {}).items():
            getattr(self.pdf, 'set_{0}'.format(key))(value)

    def prepare_elements(self):
        defaults = self.tconfig.pop('defaults', {})
        for key, telement in self.tconfig.items():
            elem = defaults.copy()
            elem.update(telement)
            try:
                def setreplace(dct, key, replace):
                    if not key in dct:
                        dct[key] = replace(dct)

            except KeyError as ke:
                raise MissingParameterError(key) from ke

            self.elements[key] = elem

    def __getitem__(self, name):
        if name in self.elements:
            return self.elements[name]['text']

    def __setitem__(self, name, value):
        if name in self.elements:
            self.elements[name]['text'] = value
        else:
            raise KeyError('{name} is no element'.format(name=name))

    def element_text(self, x, y, w, h, text, font, size, style='', align='L', foreground=None,
                     border=0, bordercolor=0, fill=False, background=None, multiline=False, **kwargs):
        if background is not None:
            self.pdf.set_fill_color(*rgb(background))
        if foreground is not None:
            self.pdf.set_text_color(*rgb(foreground))
        if bordercolor is not None:
            self.pdf.set_draw_color(*rgb(bordercolor))
        self.pdf.set_font(font, style, size)
        self.pdf.set_xy(x, y)
        if not multiline in [1, True, 'true']:
            self.pdf.cell(w=w, h=h, txt=text, border=border,
                          ln=0, align=align, fill=fill)
        else:
            self.pdf.multi_cell(w=w, h=self.pdf.k * size /
                                10 * 1.2, txt=text, border=border, align='J')

    def element_box(self, x, y, w, h, border, background=0,
                    bordercolor=0xFFFFFF, style='D', **kwargs):
        if background is not None:
            self.pdf.set_fill_color(*rgb(background))
        if bordercolor is not None:
            self.pdf.set_draw_color(*rgb(bordercolor))
        self.pdf.rect(x, y, w, h, style=style)
        pass

    def element_rect(self, **kwargs):
        self.rect(**kwargs, style='F')
        pass

    def element_image(self, x, y, w, h, text, link='', type='', **kwargs):
        self.pdf.image(text, x, y, w, h, type=type, link=link)
        pass

    def element_unknown(self, type, **kwargs):
        print('detected unknown type: {0}'.format(type))
        pass
