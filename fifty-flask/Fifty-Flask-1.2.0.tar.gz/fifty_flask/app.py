import ast
import os
from flask import Flask as DefaultFlask
from jinja2 import FileSystemBytecodeCache


class Flask(DefaultFlask):
    jinja_key_prefix = 'JINJA'

    def create_jinja_environment(self):
        """Customizes the Jinja environment.
        """
        self.jinja_options = self.get_jinja_options()
        return super(Flask, self).create_jinja_environment()

    def get_jinja_options(self):
        """Get the Jinja config from the app config.
        """
        # start by making the original options mutable
        jinja_options = dict(self.jinja_options)

        # index of the string where the Jinja variable begins
        # example: JINJA_AUTO_RELOAD = True (AUTO_RELOAD is the jinja var we need)
        jinja_key_offset = len(self.jinja_key_prefix) + 1

        # updates the jinja options with new jinja variables from the config
        # lowercases the var name from the config var name to be compatible w/ jinja's lowercase
        # requirement
        jinja_options.update({
            key[jinja_key_offset:].lower(): self.config[key]
            for key in self.config if key.startswith(self.jinja_key_prefix)
            })

        # Enable some sensible defaults when not in debug mode
        if not self.debug:
            jinja_options.setdefault('auto_reload', False)

            if 'bytecode_cache' not in jinja_options:
                directory = self.config.get('FS_BYTECODE_CACHE_DIR')
                jinja_options['bytecode_cache'] = FileSystemBytecodeCache(directory=directory)

        return jinja_options

    def configure(self, config_file_name=None, **config_kwargs):
        """Configures an app with default configuration as well as anything
        specified in config and environment variables.
        """
        # start with project defaults
        self.config.from_pyfile('config_default.py')

        # override with a different default
        if config_file_name:
            self.config.from_pyfile(config_file_name)

        # override with a local config
        self.config.from_pyfile('config_local.py', silent=True)

        # override with config options excplitly passed in the code
        self.config.update(config_kwargs)
        
        # override with the testing configs
        if self.config.get('TESTING'):
            self.config.from_pyfile('config_test_default.py', silent=True)
            self.config.from_pyfile('config_test_local.py', silent=True)

        # override with the environment variables
        env_prefix = self.config.get('ENV_PREFIX')
        if env_prefix:
            env_config = get_env_config(env_prefix)
            self.config.update(env_config)


def get_env_config(env_prefix):
    """Given an environment, this function will look for all variable names
    that start with the package name and update globals() with the key/val
    pairs.
    """
    def cast(value):
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            return value

    env_prefix = env_prefix.upper()

    offset = len(env_prefix) + 1

    return {env_var_name[offset:]: cast(env_var_value)
            for env_var_name, env_var_value in os.environ.iteritems()
            if env_var_name.startswith(env_prefix)}
