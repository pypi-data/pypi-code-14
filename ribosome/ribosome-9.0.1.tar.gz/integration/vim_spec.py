from amino import Right
from amino.test import later

from ribosome.test import PluginIntegrationSpec

from integration._support.facade import FacadeTestPlugin


class VimSpec(PluginIntegrationSpec):

    @property
    def _prefix(self):
        return 'ribosome'

    @property
    def plugin_class(self):
        return Right(FacadeTestPlugin)

    def _last_output(self, content):
        later(lambda: self._log_out.last.should.contain(content), timeout=1)

    def vars(self):
        self.vim.cmd_sync('Go')
        self.vim.buffer.vars.set_p('var1', 'content')
        print(self.vim.call('AllVars'))

__all__ = ('VimSpec',)
