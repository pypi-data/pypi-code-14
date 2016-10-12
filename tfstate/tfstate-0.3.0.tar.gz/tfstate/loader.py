import os
import hashlib
import subprocess
import time
import json
import re
from urlparse import urlparse
from . import utils

DEFAULT_CACHE_MAX_SECONDS = 60
OUTPUT_REGEX = re.compile("^(?P<key>\w+) = (?P<value>.*)$")


class TerraformLoader(object):
    @classmethod
    def initialize(cls, cache_dir, state_uri,
                   terraform_bin_path='terraform',
                   cache_max_seconds=DEFAULT_CACHE_MAX_SECONDS, options=None):
        options = options or {}

        loader = cls(cache_dir, state_uri, terraform_bin_path,
                     cache_max_seconds, options)

        loader.ensure_cache_dir_exists()
        loader.ensure_cache_dir_for_state_uri_exists()

        return loader


    def __init__(self, cache_dir, state_uri, terraform_bin_path,
                 cache_max_seconds, options):
        self._cache_dir = cache_dir
        self._state_uri = state_uri
        self._terraform_bin_path = terraform_bin_path
        state_uri_hash_obj = hashlib.md5()
        state_uri_hash_obj.update(state_uri)
        self._state_uri_hash = state_uri_hash_obj.hexdigest()
        self._state_uri_cache_dir = os.path.join(cache_dir,
                                                 self._state_uri_hash)
        self._cache_max_seconds = cache_max_seconds
        self._options = options

    def ensure_cache_dir_exists(self):
        utils.mkdir_p(self._cache_dir)

    def ensure_cache_dir_for_state_uri_exists(self):
        utils.mkdir_p(self._state_uri_cache_dir)

    def load_state(self, module=None):
        # Determine what kind of state it is based on the uri. If it's a file
        # it's local. If it's s3 let's setup a remote state
        parsed_uri = urlparse(self._state_uri)

        if parsed_uri.scheme == 'file':
            return self._load_file_state(parsed_uri.path, module=module)
        elif parsed_uri.scheme == 's3':
            return self._load_s3_state(parsed_uri.netloc, parsed_uri.path,
                                       module=module)
        else:
            # FIXME... seriously...
            raise Exception("Unhandled state uri type in %s.. sorry" % self._state_uri)

    def _load_s3_state(self, bucket, path, module=None):
        # Configure the remote state in the state uri's cache directory so that
        # `terraform output` can be run
        env = {
            'AWS_DEFAULT_REGION': self._options.get('AWS_DEFAULT_REGION',
                os.environ.get(
                    'AWS_DEFAULT_REGION',
                    'us-east-1'
                )
            )
        }

        dot_terraform_dir_path = os.path.join(self._state_uri_cache_dir,
                                              '.terraform')

        if not os.path.exists(dot_terraform_dir_path):
            command = [
                self._terraform_bin_path, 'remote', 'config',
                '-backend=S3',
                '-backend-config', 'bucket=%s' % bucket,
                '-backend-config', 'key=%s' % path[1:],
                '-backend-config', 'encrypt=true'
            ]

            try:
                self._call(command, cwd=self._state_uri_cache_dir, env=env)
            except subprocess.CalledProcessError:
                raise Exception('Failed to setup remote configuration')

        return self._get_terraform_output(
            module=module,
            env=env,
        )

    def _load_file_state(self, path, module=None):
        return self._get_terraform_output(
            state=path,
            module=module,
        )

    def _get_output_cache(self, cache_file):
        if not os.path.exists(cache_file):
            return None

        cache_file_stat = os.stat(cache_file)
        last_modification_time = cache_file_stat.st_mtime

        now = time.time()

        if now - last_modification_time > self._cache_max_seconds:
            return None
        return json.load(open(cache_file))

    def _save_output_cache(self, cache_file, output):
        json.dump(output, open(cache_file, 'w'))

    def _call(self, command, subprocess_cmd=subprocess.check_output,
              env=None, **kwargs):
        env = env or {}

        exec_env = os.environ.copy()
        exec_env.update(env)

        return subprocess_cmd(command, env=exec_env, **kwargs)

    def _get_terraform_output(self, state=None, module=None, env=None):
        output_cache_file = os.path.join(self._state_uri_cache_dir, 'root.json')

        if module:
            output_cache_file = os.path.join(self._state_uri_cache_dir,
                                             '%s.json' % module)
        output = self._get_output_cache(output_cache_file)

        if output:
            return output

        command = [
            self._terraform_bin_path, 'output', '-json'
        ]

        if state:
            command.append('-state=%s' % state)
        if module:
            command.append('-module=%s' % module)

        try:
            raw_output = self._call(command, env=env,
                                    cwd=self._state_uri_cache_dir)
        except subprocess.CalledProcessError:
            # FIXME do something smarter here
            raise

        output = self._parse_terraform_output(raw_output)
        self._save_output_cache(output_cache_file, output)
        return output

    def _parse_terraform_output(self, terraform_str_output):
        output = {}

        terraform_json_output = json.loads(terraform_str_output)
        for key, obj in terraform_json_output.iteritems():
            value = obj['value']
            if type(value) == list:
                output[key] = ','.join(value)
            else:
                output[key] = value

        return output
