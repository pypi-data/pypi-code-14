"""
Pretty Code Extension for Python-Markdown
=========================================

Adds enhenced code/syntax highlighting to standard Python-Markdown code blocks.

See <https://github.com/joywek/markdown-pretty.git> for documentation.

This code is based from **Fenced Code Extension**, and use **pygment** to make some 
enhancements to code/syntax highlighting. see the following links for more information.

    https://pythonhosted.org/Markdown/extensions/fenced_code_blocks.html
    http://pygments.org

License: [BSD](http://www.opensource.org/licenses/bsd-license.php)

"""

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.extensions.codehilite import CodeHilite, CodeHiliteExtension, parse_hl_lines
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer
import re

class CodeBlockPreprocessor(Preprocessor):
    FENCED_BLOCK_RE = re.compile(r'''
(?P<fence>^(?:~{3,}|`{3,}))[ ]*         # Opening ``` or ~~~
(\{?\.?(?P<lang>[a-zA-Z0-9_+-]*))?[ ]*  # Optional {, and lang
# Optional highlight lines, single- or double-quote-delimited
(hl_lines=(?P<quot>"|')(?P<hl_lines>.*?)(?P=quot))?[ ]*
}?[ ]*\n                                # Optional closing }
(?P<code>.*?)(?<=\n)
(?P=fence)[ ]*$''', re.MULTILINE | re.DOTALL | re.VERBOSE)
    CODE_WRAP = '<pre><code%s>%s</code></pre>'
    LANG_TAG = ' class="%s"'

    def __init__(self, md):
        super(CodeBlockPreprocessor, self).__init__(md)
        self.checked_for_codehilite = False
        self.codehilite_conf = {}

    def run(self, lines):
        # Check for code hilite extension
        if not self.checked_for_codehilite:
            for ext in self.markdown.registeredExtensions:
                if isinstance(ext, CodeHiliteExtension):
                    self.codehilite_conf = ext.config
                    break
            self.checked_for_codehilite = True

        text = "\n".join(lines)
        while 1:
            m = self.FENCED_BLOCK_RE.search(text)
            if m:
                lang = None
                lexer = None
                code = None

                try:
                    lang = m.group('lang').lower()
                    code = m.group('code')
                except IndexError:
                    if code is None:
                        break
                
                try:
                    lexer = get_lexer_by_name(lang)
                except ValueError:
                    try:
                        lexer = guess_lexer(code)
                    except ValueError:
                        lexer = lexer = get_lexer_by_name('text')

                placeholder = highlight(code, lexer, HtmlFormatter())
                text = '%s\n%s\n%s' % (text[:m.start()], placeholder, text[m.end():])
            else:
                break
        return text.split("\n")

    def _escape(self, txt):
        """ basic html escaping """
        txt = txt.replace('&', '&amp;')
        txt = txt.replace('<', '&lt;')
        txt = txt.replace('>', '&gt;')
        txt = txt.replace('"', '&quot;')
        return txt

class CodePrettyExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)
        md.preprocessors.add('pretty_code_block', CodeBlockPreprocessor(md), ">normalize_whitespace")

def makeExtension(*args, **kwargs):
    # Inform Markdown of the existence of the extension.
    return CodePrettyExtension(*args, **kwargs)

