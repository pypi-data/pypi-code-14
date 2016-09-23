from __future__ import absolute_import
import logging
import shlex
import subprocess
import os

LOG = logging.getLogger(__name__)


class CommandResult(object):
	def __init__(self, exit_code, stdout, stderr, command):
		self.exit_code = exit_code
		self.stdout = stdout.strip()
		self.stderr = stderr.strip()
		self.command = command

	@property
	def was_successful(self):
		return self.exit_code == 0

	@property
	def text(self):
		return '\n'.join([self.stdout, self.stderr])


def popen(command, env=None, copy_env=True, **kwargs):
	if isinstance(command, str):
		command = shlex.split(command)

	proc_env = os.environ if copy_env else {}
	if env:
		proc_env.update(env)

	LOG.debug('command = %r, env = %r', command, proc_env)

	return subprocess.Popen(
		command,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
		env=proc_env,
		**kwargs
	)


def get_result(proc, command):
	stdout, stderr = proc.communicate()

	return CommandResult(
		exit_code=proc.returncode,
		stdout=stdout.decode(),
		stderr=stderr.decode(),
		command=command,
	)


def run_command(command, **kwargs):
	proc = popen(command, **kwargs)

	return get_result(proc, command)
