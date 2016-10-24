# this project is licensed under the WTFPLv2, see COPYING.txt for details

import re

from PyQt5.Qsci import QsciLexerCustom

from ..colorutils import QColor
from ..qt import Slot


SHA_RE = re.compile(r'\b[0-9a-f]{8,}\b')


class BlameLexer(QsciLexerCustom):
	Normal = 0
	SHA1 = 1
	LineAdded = 2
	LineRemoved = 3
	Keyword = 4
	ContextLine = 5

	def __init__(self, **kwargs):
		super(BlameLexer, self).__init__(**kwargs)

	def setEditor(self, ed):
		super(BlameLexer, self).setEditor(ed)

		if self.editor() is not None:
			self.setColor(QColor('#000000'), self.Normal)
			self.setColor(QColor('#ff00ff'), self.SHA1)
			self.setColor(QColor('#00ff00'), self.LineAdded)
			self.setColor(QColor('#ff0000'), self.LineRemoved)
			self.setColor(QColor('#0000ff'), self.Keyword)
			self.editor().setStyleHotspot(self.SHA1, True)

	def language(self):
		return 'Git command output'

	def description(self, style):
		if style == self.Normal:
			return 'Normal'
		elif style == self.SHA1:
			return 'SHA1'
		elif style == self.LineAdded:
			return 'Line added'
		elif style == self.LineRemoved:
			return 'Line removed'
		elif style == self.Keyword:
			return 'Keyword'
		return ''

	def styleText(self, start, end):
		ed = self.editor()

		self.startStyling(start)

		sl, sc = ed.lineIndexFromPosition(start)
		self.startStyling(ed.positionFromLineIndex(sl, 0))

		el, ec = ed.lineIndexFromPosition(end)
		for i in range(sl, el + 1):
			line = ed.text(i)
			line_offset = ed.positionFromLineIndex(i, 0)
			line_end_offset = ed.positionFromLineIndex(i, len(line))
			len_bytes = line_end_offset - line_offset

			if line.startswith('+'):
				self.setStyling(len_bytes, self.LineAdded)
			elif line.startswith('-'):
				self.setStyling(len_bytes, self.LineRemoved)
			elif line.startswith('@@ '):
				self.setStyling(len_bytes, self.ContextLine)
			else:
				starting = line_offset
				mtc_offset_end = line_offset
				for mtc in SHA_RE.finditer(line):
					mtc_offset = ed.positionFromLineIndex(i, mtc.start())
					if mtc_offset - starting > 0:
						self.setStyling(mtc_offset - starting, self.Normal)

					mtc_offset_end = ed.positionFromLineIndex(i, mtc.end())
					self.setStyling(mtc_offset_end - mtc_offset, self.SHA1)

					starting = mtc_offset_end
				if line_end_offset - mtc_offset_end > 0:
					self.setStyling(line_end_offset - mtc_offset_end, self.Normal)


from .actions import registerAction
from ..widgets.editor import Editor
import os
from ..procutils import runBlocking

def displayGit(ed, dir, cmd):
	exitcode, stdout = runBlocking(cmd, cwd=dir)
	if exitcode != 0:
		return

	newed = GitEditor()
	newed.setText(stdout)
	newed.setRepository(dir)

	ed.parentTabBar().addWidget(newed)
	newed.giveFocus()



@registerAction('editor', 'openBlame')
def openBlame(ed):
	dir, file = os.path.split(ed.path)

	displayGit(ed, dir, ['git', 'blame', file])


@registerAction('editor', 'openDiff')
def openDiff(ed):
	dir, file = os.path.split(ed.path)

	displayGit(ed, dir, ['git', 'diff', file])


class GitEditor(Editor):
	def __init__(self, **kwargs):
		super(GitEditor, self).__init__(**kwargs)

		self.repo = ''

		self.setLexer(BlameLexer())
		self.setReadOnly(True)
		self.setUndoCollection(False)
		self.emptyUndoBuffer()

		self.SCN_HOTSPOTCLICK.connect(self.onHotspot)

	def setRepository(self, repo):
		self.repo = repo

	@Slot(int, int)
	def onHotspot(self, pos, modifiers):
		assert self.getStyleAt(pos) == BlameLexer.SHA1

		commit = self.wordAtPos(pos)
		displayGit(self, self.repo, ['git', 'show', commit])
