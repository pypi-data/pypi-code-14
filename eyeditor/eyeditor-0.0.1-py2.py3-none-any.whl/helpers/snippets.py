# this project is licensed under the WTFPLv2, see COPYING.txt for details

import string

from PyQt5.QtCore import QObject

from ..three import str
from ..connector import registerSignal, defaultEditorConfig
from ..qt import Slot


INDIC_VAR = 'sniptpl'
INDIC_ZONE = 'snipzone'


@defaultEditorConfig
def setupIndicator(ed):
        ed.createIndicator(INDIC_ZONE)
        ed.createIndicator(INDIC_VAR)


class Templater(QObject):
	def __init__(self, editor, snippet_text, **kwargs):
		super(Templater, self).__init__(**kwargs)
		self.editor = editor
		self.text = snippet_text
		self.formatter = string.Formatter()
		self.templating = False

	@Slot(object)
	def onModified(self, args):
		if not self.templating:
			return
		if not args.modificationType & (self.editor.SC_MOD_INSERTTEXT | self.editor.SC_MOD_DELETETEXT):
			return

		self.editor.sciModified.disconnect(self.onModified)
		self.replaceTemplate()
		self.editor.sciModified.connect(self.onModified)
		print(args)

	def clear(self):
		self.editor.indicators[INDIC_ZONE].clear()
		self.editor.indicators[INDIC_VAR].clear()

	def defaults(self):
		return max(int(field) for _, field, _, _ in self.formatter.parse(self.text) if field is not None)

	def fetchValues(self):
		textbytes = self.editor.text().encode('utf-8')
		indicator = self.editor.indicators[INDIC_VAR]

		res = []
		for start, end in indicator.iterRanges():
			res.append(textbytes[start:end])

		print('fetch', res)

		if not res:
			res = map(str, xrange(self.defaults() + 1))
		return res

	def insert(self, start_offset):
		tpl_indicator = self.editor.indicators[INDIC_VAR]

		textbytes = self.text.encode('utf-8')

		values = self.fetchValues()

		end_offset = start_offset
		for literal, field, fmt, conv in self.formatter.parse(self.text):
			literal = literal.encode('utf-8')
			self.editor.insertBytes(end_offset, literal)
			end_offset += len(literal)

			if field is None:
				continue

			obj, _ = self.formatter.get_field(field, values, {})
			formatted = self.formatter.convert_field(obj, conv)
			formatted = formatted.encode('utf-8')
			self.editor.insertBytes(end_offset, formatted)

			tpl_indicator.putAtOffset(end_offset, end_offset + len(formatted))
			end_offset += len(formatted)

		indicator = self.editor.indicators[INDIC_ZONE]
		indicator.putAtOffset(start_offset, end_offset)

	def startTemplating(self):
		self.insert(self.editor.cursorOffset())
		self.templating = True
		self.editor.sciModified.connect(self.onModified)

	def endTemplating(self):
		self.templating = False
		self.editor.sciModified.disconnect(self.onModified)
		self.clear()

	def replaceTemplate(self):
		zone = list(self.editor.indicators[INDIC_ZONE].iterRanges())
		assert len(zone) == 1

		self.clear()
		with self.editor.undoGroup():
			self.editor.deleteRange(*zone[0])
			print('del', zone)
			self.insert(zone[0][0])


#####

from .actions import registerShortcut

TEXT = '''
hello
{0}
foo
'''

@registerShortcut('editor', 'Ctrl+J')
def doSnip(ed):
	ed.tpl = Templater(ed, TEXT)
	ed.tpl.startTemplating()
