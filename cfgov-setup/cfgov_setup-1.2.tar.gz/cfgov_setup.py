import os

from distutils.command.build_ext import build_ext
from setuptools.command.bdist_egg import bdist_egg
from wheel.bdist_wheel import bdist_wheel

from setuptools import Command

from subprocess import check_call


def make_build_frontend_command(script_name):
    class build_frontend(Command):
        description = 'run %s' % script_name
        user_options = []

        def run(self):
            check_call(['sh', script_name])

        def initialize_options(self):
            """ API requires that we override this, but we have nothing to do"""
            pass

        def finalize_options(self):
            """ API requires that we override this, but we have nothing to do"""
            pass

    return build_frontend


def wrap_command(original_command):
    class new_command(original_command):
        def run(self):
            self.run_command('build_frontend')
            original_command.run(self)

    return new_command

def do_frontend_build(dist, key, script_name):
    commands = {
       'build_frontend': make_build_frontend_command(script_name),
       'build_ext': wrap_command(build_ext),
       'bdist_egg': wrap_command(bdist_egg),
       'bdist_wheel': wrap_command(bdist_wheel)
    }
    dist.cmdclass.update(commands)
