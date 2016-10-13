# -*- coding: utf-8 -*-
# Copyright (C) 2012-2016 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.Werkzeug.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.Werkzeug.deploy
#
# Purpose
#    Provide an extendable Command for the deployment of applications based
#    on GTW.Werkzeug
#
# Revision Dates
#    23-May-2012 (CT) Creation
#    24-May-2012 (CT) Add sub-command `setup_cache`
#     1-Jun-2012 (CT) Factor `_app_call` from `setup_cache`
#     1-Jun-2012 (CT) Add sub-command `fcgi`
#     1-Jun-2012 (CT) Add `py_options` to `_FCGI_._defaults`
#     1-Jun-2012 (CT) Derive from `GTW.OMP.deploy`, not `GTW.deploy`
#     1-Jun-2012 (CT) Add sub-command `ubycms`
#     3-Jun-2012 (CT) Add sub-command `fcgi_script`
#     3-Jun-2012 (CT) Use `self.lib_dir`, not `P.lib_dir`, in
#                     `_handle_fcgi_script`
#     5-Jun-2012 (CT) Add `exec` to output of `_handle_fcgi_script`
#    12-Dec-2013 (CT) Add `-script_path`, execute `chmod +x` on `fcgi_script`
#    16-Dec-2013 (CT) Add sub-command `create_config`,
#                     factor `_create_fcgi_script`
#    17-Dec-2013 (CT) Remove `lstrip_blocks` to allow jinja 2.6
#    17-Dec-2013 (CT) Add `verbose` to `_handle_create_config`
#    18-Dec-2013 (CT) Add `ca_path`, `ca_key_name` to `_handle_create_config`
#    20-Dec-2013 (CT) Split `addr_port` into `address` and `port`
#     7-Jan-2014 (CT) Use `-quiet`, not `-verbose`, for `create_config`
#     7-Jan-2014 (CT) Move `-quiet` to `_FCGI_Script_`
#     9-Jul-2014 (CT) Fix `_create_fcgi_script`: catch KeyError;
#                     recognize stdout; use `P.lib_dir`, not `self.lib_dir`
#     9-Jul-2014 (CT) Use `P.py_path`, not `P.lib_dir`
#     1-Sep-2014 (CT) Add `lib_dirs` to arguments of `templateer.call_macro`
#     2-Sep-2014 (CT) Add and use `template_package_dirs`
#     2-Sep-2014 (CT) Change `dynamic_defaults` to check `combined`
#    17-Mar-2015 (CT) Add sub-command `wsgi_script`, remove sub-command `fcgi`
#    17-Mar-2015 (CT) Add option `use_wsgi` to `create_config`
#    19-Mar-2015 (CT) Add `-apache2_4`, `-document_root` to `create_config`
#                     put `config_options` into `globals` of `templateer `
#    19-Mar-2015 (CT) Add option `-cert_extension` to `create_config`
#    26-Feb-2016 (CT) Add option `-ssl_chain` to `create_config`
#    15-Jun-2016 (CT) Rename handler argument `cmd` to `cao`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function #, unicode_literals

from   _GTW                   import GTW
from   _TFL                   import TFL

import _GTW._OMP.deploy

from   _TFL                   import sos
from   _TFL.import_module     import import_module
from   _TFL.predicate         import uniq
from   _TFL.Regexp            import Re_Replacer, re

import sys

strip_empty_lines = Re_Replacer ("^( *\n)( *\n)+", r"\1", re.MULTILINE)

class _GT2W_Sub_Command_ (GTW.OMP.deploy._Sub_Command_) :

    _rn_prefix = "_GT2W"

_Sub_Command_ = _GT2W_Sub_Command_ # end class

_Ancestor = GTW.OMP.deploy.Command

class GT2W_Command (_Ancestor) :
    """Manage deployment applications based on GTW.Werkzeug."""

    _rn_prefix              = "GT2W"

    _defaults               = dict \
        ( template_package_dirs = ["_JNJ"]
        )
    _wsgi_script_format     = """\
import sys
sys.path.insert (0, "%(app_dir)s")
from %(app_mod)s import command
sys.path = sys.path [1:]
application = command (%(args)s)
    """

    class _GT2W_HTTP_Config_ (TFL.Command.Root_Command.Config) :
        """Config file for HTTP-config specific options"""

        rank                    = -80
        _name                   = "HTTP_Config"

    HTTP_Config = _GT2W_HTTP_Config_ # end class

    class _GT2W_Babel_ (_Sub_Command_, _Ancestor._Babel_) :

        _package_dirs           = [ "_JNJ", "_ReST"]

    _Babel_ = _GT2W_Babel_ # end class

    class _GT2W_xxGI_ (_Sub_Command_) :
        """Run application as a FastCGI server."""

        is_partial              = True

        _defaults               = dict \
            ( apply_to_version  = "active"
            )

        _opts                   = \
            ( "-quiet:B?Don't write information about files created"
            , "-script_path:Q?Path of script created"
            )

    _GT2W_xxGI_ # end class

    class _GT2W_FCGI_Script_ (_GT2W_xxGI_) :
        """Create script for running the application as a FastCGI server."""

    _FCGI_Script_ = _GT2W_FCGI_Script_ # end class

    class _GT2W_Create_Config_ (_GT2W_xxGI_) :
        """Create config file and fcgi- or wsgi-script for http-server"""

        _defaults               = dict \
            ( address           = "*"
            , ca_key_name       = "CA_crt"
            , ca_path           = "~/CA"
            , cert_extension    = "pem"
            , document_root     = "~/"
            , host_macro        = "gtw_host"
            , macro_module      = "httpd_config/apache.m.jnj"
            , port              = "80"
            , root_dir          = "~/active"
            )

        _opts                   = \
            ( "-address:S?Address of virtual host"
            , "-apache2_4:B?Create config for Apache 2.4"
            , "-ca_key_name:S?Name of CA key file"
            , "-ca_path:Q?Path for server-specific CA for client certificates"
            , "-cert_extension:S?Extension of SSLCertificateFile (pem or crt)"
            , "-config_path:Q?Path for config file"
            , "-document_root:Q?"
                "Path for DocumentRoot of virtual host. For Apache 2.4, "
                "`DocumentRoot` must include both `root_dir` and `script_path`."
            , "-group:S?Define unix group that the wsgi process should be run as"
            , "-host_macro:S?Name of macro to create virtual host"
            , "-macro_module:S"
                "?Name of jinja module providing config-generation macros"
            , "-port:S?Port for virtual host"
            , "-root_dir:Q?Root directory of the web app. This is the path "
                "to the directory containing www/app and the library "
                "directories specified by the option `-lib_dir`."
            , "-server_admin:S?Email address of server admin of virtual host"
            , "-server_aliases:T#8?Alias names for virtual host"
            , "-server_name:S?Fully qualified domain name of virtual host"
            , "-ssl_key_name:S?Name of SSL key to use for HTTPS"
            , "-ssl_chain:T#4?Names of files containing SSL chain certificates"
            , "-use_wsgi:B?Define unix user that the wsgi process should be run as"
            , "-user:S?Run wsgi process as user specified "
            , "-template_dirs:P?Directories containing templates for config"
            )

        def dynamic_defaults (self, defaults) :
            def _gen_template_dirs (self, defaults) :
                yield self.app_dir
                tpds = defaults.get ("template_package_dirs", ["_JNJ"])
                for tpd in tpds :
                    mod = import_module (tpd)
                    yield sos.path.dirname (mod.__file__)
            result   = self.__super.dynamic_defaults (defaults)
            combined = dict (defaults, ** result)
            tdirs    = list (combined.get ("template_dirs", ()))
            tdirs.extend  (_gen_template_dirs (self, combined))
            result ["template_dirs"] = tuple (uniq (tdirs))
            return result
        # end def dynamic_defaults

    _Create_Config_ = _GT2W_Create_Config_ # end class

    class _GT2W_Setup_Cache_ (_Sub_Command_) :
        """Setup the cache of the application."""

    _Setup_Cache_ = _GT2W_Setup_Cache_ # end class

    class _GT2W_UBYCMS_ (TFL.Command.Sub_Command_Combiner) :
        """Update, Babel compile, pYcompile, setup Cache, Migrate, Switch."""

        _rn_prefix       = "_GT2W"

        _sub_command_seq = \
            [ "update"
            , "pycompile"
            , ["babel", "compile"]
            , ["migrate", "-Active", "-Passive"]
            , "setup_cache"
            , "switch"
            ]

    _UBYCMS_ = _GT2W_UBYCMS_ # end class

    class _GT2W_WSGI_Script_ (_GT2W_xxGI_) :
        """Create script for running the application as a wsgi server."""


    _WSGI_Script_ = _GT2W_WSGI_Script_ # end class

    def _create_fcgi_script (self, cao, argv = (), script_path = None) :
        P      = self._P (cao)
        a_conf = cao.app_config
        try :
            h_conf = cao._spec ["HTTP_Config"].pathes
        except KeyError :
            h_conf = []
        config = self.App_Config.auto_split.join (a_conf + h_conf)
        args   = ("fcgi", "-config", config) + tuple (argv)
        app    = self._app_cmd (cao, P, args = args)
        s_path = script_path or cao.script_path
        def write (f, app, py_path) :
            f.write ("#!/bin/sh\n")
            f.write ("export PYTHONPATH=%s\n" % (py_path, ))
            f.write ("exec %s\n" % (app, ))
        if s_path and not s_path.endswith (("-", "stdout")) :
            with open (s_path, "w") as f :
                write (f, app, P.py_path)
            self.pbl ["chmod"] ("+x", s_path)
            if not cao.quiet :
                print ("Created fcgi script", s_path)
        else :
            write (sys.stdout, app, P.py_path)
    # end def _create_fcgi_script

    def _create_wsgi_script (self, cao, argv = (), script_path = None) :
        P      = self._P (cao)
        a_conf = cao.app_config
        try :
            h_conf = cao._spec ["HTTP_Config"].pathes
        except KeyError :
            h_conf = []
        config   = self.App_Config.auto_split.join (a_conf + h_conf)
        app_dir  = sos.path.dirname  (self._app_path (cao, P))
        app_mod  = sos.path.splitext (sos.path.basename (cao.app_module)) [0]
        args     = ("wsgi", "-config", config) + tuple (argv)
        s_path   = script_path or cao.script_path
        def write (f, app_dir, app_mod, args) :
            script = self._wsgi_script_format % dict \
                ( app_dir = app_dir
                , app_mod = app_mod
                , args    = list (args) if args else ""
                )
            f.write (script.strip ())
            f.write ("\n")
        if s_path and not s_path.endswith (("-", "stdout")) :
            with open (s_path, "w") as f :
                write (f, app_dir, app_mod, args)
            if not cao.quiet :
                print ("Created wsgi script", s_path)
        else :
            write (sys.stdout, app_dir, app_mod, args)
    # end def _create_wsgi_script

    def _handle_create_config (self, cao) :
        if cao.use_wsgi :
            _create_script  = self._create_wsgi_script
            xxgi_macro_name = "use_wsgi"
        else :
            _create_script  = self._create_fcgi_script
            xxgi_macro_name = "use_fcgi"
        _create_script (cao, cao.argv, cao.script_path)
        from   _JNJ import JNJ
        import _JNJ.Templateer
        config_options       = dict \
            ( address        = cao.address
            , admin          = cao.server_admin
            , aliases        = cao.server_aliases
            , apache2_4      = cao.apache2_4
            , app_root       = cao.root_dir
            , ca_key_name    = cao.ca_key_name
            , ca_path        = cao.ca_path
            , cert_extension = cao.cert_extension
            , cmd            = cao
            , doc_root       = cao.document_root
            , group          = cao.group
            , lib_dirs       = cao.lib_dir
            , macro_name     = cao.host_macro
            , port           = cao.port
            , script         = cao.script_path
            , server_name    = cao.server_name
            , ssl_key_name   = cao.ssl_key_name
            , ssl_chain      = cao.ssl_chain
            , templ_name     = cao.macro_module
            , user           = cao.user
            )
        templateer           = JNJ.Templateer \
            ( encoding       = cao.input_encoding
            , globals        = dict (config_options = config_options)
            , load_path      = cao.template_dirs
            , trim_blocks    = True
            )
        xxgi_macro           = templateer.GTW.get_macro \
            (xxgi_macro_name, templ_name = cao.macro_module)
        config_options.update (xxgi_macro = xxgi_macro)
        config   = templateer.call_macro (** config_options)
        config_s = strip_empty_lines (config).strip ()
        c_path   = cao.config_path
        def write (f, config) :
            f.write (config)
            f.write ("\n")
        if c_path and c_path not in ("-", "stdout") :
            with open (c_path, "w") as f :
                write (f, config_s)
            if not cao.quiet :
                ### Can't use `cao.verbose` here because that would be
                ### included in the fcgi script
                print ("Created config file", c_path)
        else :
            write (sys.stdout, config_s)
    # end def _handle_create_config

    def _handle_fcgi_script (self, cao) :
        self._create_fcgi_script (cao, cao.argv, cao.script_path)
    # end def _handle_fcgi_script

    def _handle_setup_cache (self, cao) :
        P    = self._P (cao)
        app  = self._app_cmd (cao, P)
        args = ("setup_cache", ) + tuple (cao.argv)
        self._app_call (cao, P, app, args)
    # end def _handle_setup_cache

    def _handle_wsgi_script (self, cao) :
        self._create_wsgi_script (cao, cao.argv, cao.script_path)
    # end def _handle_wsgi_script

Command = GT2W_Command # end class

if __name__ != "__main__" :
    GTW.Werkzeug._Export_Module ()
### __END__ GTW.Werkzeug.deploy
