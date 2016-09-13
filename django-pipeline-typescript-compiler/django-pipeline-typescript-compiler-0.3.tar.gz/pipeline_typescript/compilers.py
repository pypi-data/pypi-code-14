from __future__ import unicode_literals

from django.conf import settings as _settings
from pipeline.compilers import SubProcessCompiler

DEFAULTS = {
    'TYPESCRIPT_BINARY': ('/usr/bin/env', 'tsc'),
    'TYPESCRIPT_ARGUMENTS': (None,)
}


class TypescriptCompiler(SubProcessCompiler):
    output_extension = 'js'

    def match_file(self, path):
        return path.endswith('.ts')

    def compile_file(self, infile, outfile, outdated=False, force=False):
        if not outdated and not force:
            return
        settings = _settings.get(PIPELINE)
        command = (
            _settings.get('TYPESCRIPT_BINARY',
                          DEFAULTS["TYPESCRIPT_BINARY"]),
            _settings.get('TYPESCRIPT_ARGUMENTS',
                          DEFAULTS["TYPESCRIPT_ARGUMENTS"]),
            infile,
            )
        return self.execute_command(command)
