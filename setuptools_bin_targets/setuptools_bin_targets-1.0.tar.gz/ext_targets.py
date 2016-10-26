import os
from distutils import log
from setuptools import Extension
from distutils.dep_util import newer_group
from distutils.errors import DistutilsSetupError
from setuptools.command.build_ext import build_ext as _build_ext


class Executable(Extension):
    """
    This target will link the extension as a standalone application
    """
    pass


class StaticLib(Extension):
    """
    This target will link the extension as a static lib, eg lib.a
    """
    def __init__(self, *args, **kwargs):
        self.output_dir = kwargs.pop('output_dir', '.')
        super(StaticLib, self).__init__(*args, **kwargs)


class build_ext(_build_ext):

    def build_extension(self, ext):
        sources = ext.sources
        if sources is None or not isinstance(sources, (list, tuple)):
            raise DistutilsSetupError(
                  "in 'ext_modules' option (extension '%s'), "
                  "'sources' must be present and must be "
                  "a list of source filenames" % ext.name)
        sources = list(sources)

        ext_path = ext.name
        if isinstance(ext, StaticLib):
            ext_path = self.compiler.library_filename(ext_path, output_dir=ext.output_dir)

        depends = sources + ext.depends
        if not (self.force or newer_group(depends, ext_path, 'newer')):
            log.debug("skipping '%s' extension (up-to-date)", ext.name)
            return
        else:
            log.info("building '%s' extension", ext.name)

        # First, scan the sources for SWIG definition files (.i), run
        # SWIG on 'em to create .c files, and modify the sources list
        # accordingly.
        sources = self.swig_sources(sources, ext)

        # Next, compile the source code to object files.

        # XXX not honouring 'define_macros' or 'undef_macros' -- the
        # CCompiler API needs to change to accommodate this, and I
        # want to do one thing at a time!

        # Two possible sources for extra compiler arguments:
        #   - 'extra_compile_args' in Extension object
        #   - CFLAGS environment variable (not particularly
        #     elegant, but people seem to expect it and I
        #     guess it's useful)
        # The environment variable should take precedence, and
        # any sensible compiler will give precedence to later
        # command line args.  Hence we combine them in order:
        extra_args = ext.extra_compile_args or []

        macros = ext.define_macros[:]
        for undef in ext.undef_macros:
            macros.append((undef,))

        objects = self.compiler.compile(sources,
                                         output_dir=self.build_temp,
                                         macros=macros,
                                         include_dirs=ext.include_dirs,
                                         debug=self.debug,
                                         extra_postargs=extra_args,
                                         depends=ext.depends)

        # XXX outdated variable, kept here in case third-part code
        # needs it.
        self._built_objects = objects[:]

        # Now link the object files together into the desired target --
        # of course, first we have to figure out all the other things
        # that go into the mix.
        if ext.extra_objects:
            objects.extend(ext.extra_objects)
        extra_args = ext.extra_link_args or []

        # Detect target language, if not provided
        language = ext.language or self.compiler.detect_language(sources)

        if isinstance(ext, StaticLib):
            self.compiler.create_static_lib(
                objects, ext.name,
                output_dir=ext.output_dir,
                debug=self.debug,
                target_lang=language)

        elif isinstance(ext, Executable):
            self.compiler.link_executable(
                objects, ext_path,
                libraries=self.get_libraries(ext),
                library_dirs=ext.library_dirs,
                runtime_library_dirs=ext.runtime_library_dirs,
                extra_postargs=extra_args,
                debug=self.debug,
                target_lang=language)

        else:  # Shared object - regular build
            self.compiler.link_shared_object(
                objects, ext_path,
                libraries=self.get_libraries(ext),
                library_dirs=ext.library_dirs,
                runtime_library_dirs=ext.runtime_library_dirs,
                extra_postargs=extra_args,
                export_symbols=self.get_export_symbols(ext),
                debug=self.debug,
                build_temp=self.build_temp,
                target_lang=language)