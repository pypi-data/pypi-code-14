"""

Parts of this copied from prompt_toolkit, which is BSD licensed:

Copyright (c) 2014, Jonathan Slenders
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this
  list of conditions and the following disclaimer in the documentation and/or
  other materials provided with the distribution.

* Neither the name of the {organization} nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import functools
import re
import subprocess
from prompt_toolkit.interface import CommandLineInterface
from prompt_toolkit.application import Application
from prompt_toolkit.buffer_mapping import BufferMapping
from prompt_toolkit.shortcuts import create_eventloop
from prompt_toolkit.keys import Keys
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.enums import DEFAULT_BUFFER, SEARCH_BUFFER, DUMMY_BUFFER
from prompt_toolkit.filters import HasFocus
from prompt_toolkit.layout.containers import VSplit, HSplit, Window, ConditionalContainer
from prompt_toolkit.layout.controls import (BufferControl, FillControl,
    TokenListControl, UIControl, UIContent)
from prompt_toolkit.layout.dimension import LayoutDimension as D
from prompt_toolkit.layout.processors import BeforeInput
from prompt_toolkit.layout.screen import Point, Char
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token
from prompt_toolkit.utils import get_cwidth

from .envs import find_envs

def _trim_text(text, max_width):
    """
    Trim the text to `max_width`, append dots when the text is too long.
    Returns (text, width) tuple.
    
    Copied from prompt_toolkit
    """
    width = get_cwidth(text)

    # When the text is too wide, trim it.
    if width > max_width:
        # When there are no double width characters, just use slice operation.
        if len(text) == width:
            trimmed_text = (text[:max(1, max_width-3)] + '...')[:max_width]
            return trimmed_text, len(trimmed_text)

        # Otherwise, loop until we have the desired width. (Rather
        # inefficient, but ok for now.)
        else:
            trimmed_text = ''
            for c in text:
                if get_cwidth(trimmed_text + c) <= max_width - 3:
                    trimmed_text += c
            trimmed_text += '...'

            return (trimmed_text, get_cwidth(trimmed_text))
    else:
        return text, width

class MenuControl(UIControl):
    def __init__(self, items):
        self.items = items
        self.selected_ix = 0
    
    def visible_indices(self, cli):
        search = cli.buffers[SEARCH_BUFFER].document.text
        i = 0
        for j, item in enumerate(self.items):
            if item.display.startswith(search):
                yield i, j
                i += 1
    
    def create_content(self, cli, width, height):
        items = self.items
        visible_indices = dict(self.visible_indices(cli))
        #visible_items = [items[i] for i in self.visible_indices(cli)]
        
        def get_line(i):
            if i not in visible_indices:
                return [(Token.MenuItem, ' ' * width)]
            j = visible_indices[i]
            is_selected = (j == self.selected_ix)
            item = self.items[j]
            return self._get_menu_item_tokens(item, is_selected, width)
        
        return UIContent(get_line=get_line,
                         cursor_position=Point(x=0, y=self.selected_ix or 0),
                         line_count=len(visible_indices),
                         default_char=Char(' ', Token))
        
    def _get_menu_item_tokens(self, item, is_selected, width):
        if is_selected:
            token = Token.MenuItem.Current
        else:
            token = Token.MenuItem

        text, tw = _trim_text(item.display, width - 2)
        padding = ' ' * (width - 2 - tw)
        return [(token, ' %s%s ' % (text, padding))]
    
    def preferred_height(self, cli, width, max_available_height, wrap_lines):
        return max(len(self.items), max_available_height)

    @property
    def selected(self):
        return self.items[self.selected_ix]

    def select_visible(self, cli, direction='forwards'):
        visible_indices = set(j for (i,j) in self.visible_indices(cli))
        ix = self.selected_ix
        if direction=='forwards':
            lim = max(visible_indices)
            if ix > lim:
                self.selected_ix = lim
                return
            delta = +1
        else:
            lim = min(visible_indices)
            if ix < lim:
                self.selected_ix = lim
                return
            delta = -1
        
        while ix not in visible_indices:
            ix += delta
        self.selected_ix = ix

def exit_(event):
    """
    Pressing Ctrl-Q will exit the user interface.

    Setting a return value means: quit the event loop that drives the user
    interface and return this value from the `CommandLineInterface.run()` call.
    """
    event.cli.set_return_value(None)

def up(event):
    menu = event.cli.menu_control
    menu.selected_ix -= 1
    menu.select_visible(event.cli, direction='backwards')

def down(event):
    menu = event.cli.menu_control
    menu.selected_ix += 1
    menu.select_visible(event.cli, direction='forwards')

def select(event):
    menu = event.cli.menu_control
    event.cli.set_return_value(menu.selected)

def newenv(name):
    subprocess.run(['conda', 'create', '-n', name, 'python=3'])

def newenv_event(event):
    name = event.cli.current_buffer.document.text
    event.cli.run_in_terminal(functools.partial(newenv, name))
    event.cli.current_buffer.reset()
    event.cli.focus(DUMMY_BUFFER)
    event.cli.menu_control.items = find_envs()
    event.cli.menu_control.selected_ix = 0

def delete(event):
    menu = event.cli.menu_control
    menu.selected.delete()
    menu.items = find_envs()

def start_search(event):
    event.cli.focus(SEARCH_BUFFER)

def start_newenv(event):
    event.cli.focus(DEFAULT_BUFFER)

def cancel_entry(event):
    event.cli.current_buffer.reset()
    event.cli.focus(DUMMY_BUFFER)

searching = HasFocus(SEARCH_BUFFER)
new_entry = HasFocus(DEFAULT_BUFFER)
no_focus = ~(searching | new_entry)

def bind_shortcuts(registry):
    registry.add_binding('q', filter=no_focus)(exit_)
    registry.add_binding(Keys.Up)(up)
    registry.add_binding(Keys.Down)(down)
    registry.add_binding(Keys.ControlJ, filter=~new_entry)(select)
    registry.add_binding(Keys.ControlJ, filter=new_entry)(newenv_event)
    registry.add_binding(Keys.Delete, filter=~new_entry)(delete)
    registry.add_binding('/', filter=no_focus)(start_search)
    registry.add_binding('n', filter=no_focus)(start_newenv)
    registry.add_binding(Keys.ControlC, filter=(searching|new_entry))(cancel_entry)

def shortcut_tokens(s):
    m = re.match(r'\[(.+)\](.+)$', s)
    if m:
        return [
            (Token.Toolbar.Key, m.group(1)),
            (Token.Toolbar, m.group(2)),
        ]
    raise ValueError("Didn't recognise shortcut %r" % s)

def make_toolbar_tokens(cli):
    if cli.current_buffer_name == SEARCH_BUFFER:
        return shortcut_tokens('[Enter]:Select') + [
            (Token.Toolbar, '  '),
        ] + shortcut_tokens('[Ctrl-C]:Cancel search')
    elif cli.current_buffer_name == DEFAULT_BUFFER:
        return shortcut_tokens('[Enter]:Create') + [
            (Token.Toolbar, '  '),
        ] + shortcut_tokens('[Ctrl-C]:Cancel')
    else:
        return shortcut_tokens('[Enter]:Select') + [
            (Token.Toolbar, '  '),
        ] + shortcut_tokens('[N]ew') + [
            (Token.Toolbar, '  '),
        ] + shortcut_tokens('[Del]ete') + [
            (Token.Toolbar, '  '),
        ] + shortcut_tokens('[Q]uit') + [
            (Token.Toolbar, '  '),
        ] + shortcut_tokens('[/]:Search')

def text_entry_toolbar(buffer_name, prompt):
    return ConditionalContainer(Window(
        BufferControl(buffer_name=buffer_name,
                      input_processors=[BeforeInput(lambda cli: [(Token.Prompt, prompt)])],
        )),
    filter=HasFocus(buffer_name))

def create_menu_cli():
    manager = KeyBindingManager()
    registry = manager.registry
    bind_shortcuts(registry)
    menu = MenuControl(find_envs())

    layout = HSplit([
        # One window that holds the BufferControl with the default buffer on the
        # left.
        Window(content=menu),

        # A vertical line in the middle. We explicitely specify the width, to make
        # sure that the layout engine will not try to divide the whole width by
        # three for all these windows. The `FillControl` will simply fill the whole
        # window by repeating this character.
        Window(height=D.exact(1),
               content=FillControl('-', token=Token.Line)),

        # Search toolbar
        text_entry_toolbar(SEARCH_BUFFER, 'Search: '),

        # New environment toolbar
        text_entry_toolbar(DEFAULT_BUFFER, 'New environment name: '),

        # Display the text 'Hello world' on the right.
        Window(content=TokenListControl(
            get_tokens=make_toolbar_tokens)),
    ])

    style = style_from_dict({
        Token.MenuItem: '',
        Token.MenuItem.Current: 'reverse',
        Token.Toolbar.Key: 'bold',
    })

    loop = create_eventloop()
    application = Application(key_bindings_registry=registry, layout=layout,
                              buffers=BufferMapping(initial=DUMMY_BUFFER),
                            use_alternate_screen=True, style=style)
    cli = CommandLineInterface(application=application, eventloop=loop)
    cli.menu_control = menu
    return cli
