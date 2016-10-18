"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -m cwmon_system` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``cwmon_system.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``cwmon_system.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import click

from cwmon_system.metrics import CpuContextSwitchesMetric
from cwmon_system.metrics import CpuPercentageMetric
from cwmon_system.metrics import DiskPercentFreeInodesMetric
from cwmon_system.metrics import DiskPercentFreeSpaceMetric
from cwmon_system.metrics import FifteenMinuteLoadAvgMetric
from cwmon_system.metrics import FiveMinuteLoadAvgMetric
from cwmon_system.metrics import MemoryAvailableMetric
from cwmon_system.metrics import MemoryAvailablePercentageMetric
from cwmon_system.metrics import OneMinuteLoadAvgMetric
from cwmon_system.metrics import TotalProcessesMetric
from cwmon_system.metrics import ZombieProcessesMetric


@click.group(chain=True)
@click.pass_context
def system(ctx, host, user, passwd, db, port):
    """Group for system-level monitoring commands for ``cwmon``."""
    pass


@system.command()
@click.argument('path',
                type=click.Path(exists=True, file_okay=False))
@click.pass_obj
def free_space(options, path):
    """Calculate the percentage of each device that is free."""
    if not path:
        path = ["/"]

    m = DiskPercentFreeSpaceMetric(path)
    if options.dry_run:
        click.echo(m)
    else:
        m.put()


@system.command()
@click.argument('path',
                type=click.Path(exists=True, file_okay=False))
@click.pass_obj
def free_inodes(options, path):
    """Calculate the percentage of inodes on each device that are free."""
    if not path:
        path = ["/"]

    m = DiskPercentFreeInodesMetric(path)
    if options.dry_run:
        click.echo(m)
    else:
        m.put()


@system.command()
@click.pass_obj
def total_procs(options):
    """Count the total number of processes."""
    m = TotalProcessesMetric()
    if options.dry_run:
        click.echo(m)
    else:
        m.put()


@system.command()
@click.pass_obj
def zombie_procs(options):
    """Count the number of zombie processes."""
    m = ZombieProcessesMetric()
    if options.dry_run:
        click.echo(m)
    else:
        m.put()


@system.command()
@click.pass_obj
def load_avg_1(options):
    """Get the 1-minute load average."""
    m = OneMinuteLoadAvgMetric()
    if options.dry_run:
        click.echo(m)
    else:
        m.put()


@system.command()
@click.pass_obj
def load_avg_5(options):
    """Get the 5-minute load average."""
    m = FiveMinuteLoadAvgMetric()
    if options.dry_run:
        click.echo(m)
    else:
        m.put()


@system.command()
@click.pass_obj
def load_avg_15(options):
    """Get the 15-minute load average."""
    m = FifteenMinuteLoadAvgMetric()
    if options.dry_run:
        click.echo(m)
    else:
        m.put()


@system.command()
@click.pass_obj
def cpu_percent(options):
    """Get the percentage utilization of the CPU.

    ..note:: This is across all CPUs, not per-CPU.
    """
    m = CpuPercentageMetric()
    if options.dry_run:
        click.echo(m)
    else:
        m.put()


@system.command()
@click.pass_obj
def cpu_ctx_switches(options):
    """Get the number of CPU context switches since boot.

    ..note:: This is across all CPUs, not per-CPU.
    """
    m = CpuContextSwitchesMetric()
    if options.dry_run:
        click.echo(m)
    else:
        m.put()


@system.command()
@click.pass_obj
def mem_available(options):
    """Get amount of RAM that is 'available'."""
    m = MemoryAvailableMetric()
    if options.dry_run:
        click.echo(m)
    else:
        m.put()


@system.command()
@click.pass_obj
def mem_available_percent(options):
    """Get amount of RAM that is 'available' as a percentage of total RAM."""
    m = MemoryAvailablePercentageMetric()
    if options.dry_run:
        click.echo(m)
    else:
        m.put()
