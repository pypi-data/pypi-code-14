# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see spyder/__init__.py for details)

"""Find in Files Plugin"""

# pylint: disable=C0103
# pylint: disable=R0903
# pylint: disable=R0911
# pylint: disable=R0201

# Standard library imports
import sys

# Third party imports
from qtpy.QtWidgets import QApplication
from qtpy.QtCore import Signal, Slot

# Local imports
from spyder.config.base import _
from spyder.config.utils import get_edit_extensions
from spyder.py3compat import getcwd
from spyder.utils import icon_manager as ima
from spyder.utils.qthelpers import create_action
from spyder.widgets.findinfiles import FindInFilesWidget
from spyder.plugins import SpyderPluginMixin


class FindInFiles(FindInFilesWidget, SpyderPluginMixin):
    """Find in files DockWidget"""
    CONF_SECTION = 'find_in_files'
    sig_option_changed = Signal(str, object)
    toggle_visibility = Signal(bool)
    edit_goto = Signal(str, int, str)
    redirect_stdio = Signal(bool)
    
    def __init__(self, parent=None):
        supported_encodings = self.get_option('supported_encodings')
        
        search_path = self.get_option('search_path', None)        
        self.search_text_samples = self.get_option('search_text_samples')
        search_text = self.get_option('search_text')
        search_text = [txt for txt in search_text \
                       if txt not in self.search_text_samples]
        search_text += self.search_text_samples

        search_text_regexp = self.get_option('search_text_regexp')
        include = self.get_option('include')
        if not include:
            include = self.include_patterns()
        include_idx = self.get_option('include_idx', None)
        include_regexp = self.get_option('include_regexp')
        exclude = self.get_option('exclude')
        exclude_idx = self.get_option('exclude_idx', None)
        exclude_regexp = self.get_option('exclude_regexp')
        in_python_path = self.get_option('in_python_path')
        more_options = self.get_option('more_options')
        FindInFilesWidget.__init__(self, parent,
                                   search_text, search_text_regexp, search_path,
                                   include, include_idx, include_regexp,
                                   exclude, exclude_idx, exclude_regexp,
                                   supported_encodings,
                                   in_python_path, more_options)
        SpyderPluginMixin.__init__(self, parent)
        
        # Initialize plugin
        self.initialize_plugin()
        
        self.toggle_visibility.connect(self.toggle)
        
    def toggle(self, state):
        """Toggle widget visibility"""
        if self.dockwidget:
            self.dockwidget.setVisible(state)
    
    def refreshdir(self):
        """Refresh search directory"""
        self.find_options.set_directory(getcwd())

    @Slot()
    def findinfiles_callback(self):
        """Find in files callback"""
        widget = QApplication.focusWidget()
        if not self.ismaximized:
            self.dockwidget.setVisible(True)
            self.dockwidget.raise_()
        text = ''
        try:
            if widget.has_selected_text():
                text = widget.get_selected_text()
        except AttributeError:
            # This is not a text widget deriving from TextEditBaseWidget
            pass
        self.set_search_text(text)
        if text:
            self.find()

    @staticmethod
    def include_patterns():
        """Generate regex common usage patterns to include section."""
        # Change special characters, like + and . to convert into valid re
        clean_exts = []
        for ext in get_edit_extensions():
            ext = ext.replace('.', r'\.')
            ext = ext.replace('+', r'\+')
            clean_exts.append(ext)

        patterns = [r'|'.join([ext + r'$' for ext in clean_exts if ext]) +
                    r'|README|INSTALL',
                    r'\.ipy$|\.pyw?$|\.rst$|\.txt$',
                    '.',
                    ]
        return patterns

    #------ SpyderPluginMixin API ---------------------------------------------
    def switch_to_plugin(self):
        """Switch to plugin
        This method is called when pressing plugin's shortcut key"""
        self.findinfiles_callback()  # Necessary at least with PyQt5 on Windows
        SpyderPluginMixin.switch_to_plugin(self)

    #------ SpyderPluginWidget API --------------------------------------------
    def get_plugin_title(self):
        """Return widget title"""
        return _("Find in files")
    
    def get_focus_widget(self):
        """
        Return the widget to give focus to when
        this plugin's dockwidget is raised on top-level
        """
        return self.find_options.search_text
    
    def get_plugin_actions(self):
        """Return a list of actions related to plugin"""
        return []
    
    def register_plugin(self):
        """Register plugin in Spyder's main window"""
        self.get_pythonpath_callback = self.main.get_spyder_pythonpath
        self.main.add_dockwidget(self)
        self.edit_goto.connect(self.main.editor.load)
        self.redirect_stdio.connect(self.main.redirect_internalshell_stdio)
        self.main.workingdirectory.refresh_findinfiles.connect(self.refreshdir)
        
        findinfiles_action = create_action(self, _("&Find in files"),
                                   icon=ima.icon('findf'),
                                   triggered=self.findinfiles_callback,
                                   tip=_("Search text in multiple files"))        
        
        self.main.search_menu_actions += [None, findinfiles_action]
        self.main.search_toolbar_actions += [None, findinfiles_action]
    
    def refresh_plugin(self):
        """Refresh widget"""
        pass
        
    def closing_plugin(self, cancelable=False):
        """Perform actions before parent main window is closed"""
        self.closing_widget()  # stop search thread and clean-up
        options = self.find_options.get_options(all=True)
        if options is not None:
            search_text, text_re, search_path, \
            include, include_idx, include_re, \
            exclude, exclude_idx, exclude_re, \
            in_python_path, more_options = options
            hist_limit = 15
            search_text = search_text[:hist_limit]
            search_path = search_path[:hist_limit]
            include = include[:hist_limit]
            exclude = exclude[:hist_limit]
            self.set_option('search_text', search_text)
            self.set_option('search_text_regexp', text_re)
            self.set_option('search_path', search_path)
            self.set_option('include', include)
            self.set_option('include_idx', include_idx)
            self.set_option('include_regexp', include_re)
            self.set_option('exclude', exclude)
            self.set_option('exclude_idx', exclude_idx)
            self.set_option('exclude_regexp', exclude_re)
            self.set_option('in_python_path', in_python_path)
            self.set_option('more_options', more_options)
        return True


def test():
    from spyder.utils.qthelpers import qapplication
    app = qapplication()
    widget = FindInFiles()
    widget.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    test()
