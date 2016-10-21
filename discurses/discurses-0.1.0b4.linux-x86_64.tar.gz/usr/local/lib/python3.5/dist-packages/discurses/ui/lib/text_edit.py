import urwid
import discurses.keymaps as keymaps


class TextEditWidget(urwid.WidgetWrap):

    def __init__(self, callback, content=""):
        self.callback = callback
        self.w_edit = urwid.Edit(edit_text=content)
        self.w_lb = urwid.LineBox(self.w_edit)
        self.__super.__init__(self.w_lb)

    def selectable(self):
        return True

    @keymaps.TEXT_EDIT_WIDGET.keypress
    def keypress(self, size, key):
        return self.w_edit.keypress(size, key)

    @keymaps.TEXT_EDIT_WIDGET.command
    def save(self):
        self.callback(self.w_edit.edit_text)
        self.w_edit.set_edit_text("")

    @keymaps.TEXT_EDIT_WIDGET.command
    def cancel(self):
        self.callback(None)
