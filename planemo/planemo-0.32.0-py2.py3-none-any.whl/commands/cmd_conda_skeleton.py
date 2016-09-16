"""Module describing the planemo ``conda_skeleton`` command."""
from __future__ import print_function

import click

from galaxy.tools.deps import conda_util

from planemo import options
from planemo.cli import command_function
from planemo.conda import build_conda_context, collect_conda_targets
from planemo.io import error
from planemo.io import ps1_for_path


@click.command('conda_skeleton')
@options.conda_target_options()
@options.optional_tools_arg()
@click.argument(
    "source",
    metavar="SOURCE",
    type=str,
)
@command_function
def cli(ctx, path, **kwds):
    """How to activate conda environment for tool.

    Source output to activate a conda environment for this tool.

        % . <(planemo conda_env bowtie2.xml)
        % which bowtie2
        TODO_PLACE_PATH_HERE
    """
    conda_context = build_conda_context(ctx, use_planemo_shell_exec=False, **kwds)
    conda_targets = collect_conda_targets(
        path, conda_context=conda_context
    )
    installed_conda_targets = conda_util.filter_installed_targets(
        conda_targets, conda_context=conda_context
    )
    env_name, exit_code = conda_util.build_isolated_environment(
        installed_conda_targets, conda_context=conda_context
    )
    if exit_code:
        error("Failed to build environmnt for request.")
        return 1

    ps1 = ps1_for_path(path, base="PRE_CONDA_PS1")
    remove_env = "%s env remove -y --name '%s'" % (
        conda_context.conda_exec, env_name
    )
    deactivate = conda_context.deactivate
    activate = conda_context.activate
    command = SOURCE_COMMAND % (
        activate, env_name, ps1,
        deactivate, remove_env
    )
    print(command)
