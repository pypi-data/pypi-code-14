#!/usr/bin/env python3

import click

from .exceptions import FFProbeException
from .convert import convert_video, need_to_transcode, get_ffmpeg_cmd
from .media_info import get_transcode_info, get_media_info, determine_transcodings
from .preferences import THREADS
from .watch import watch_directory
from .version import __version__


@click.group(help="Convert and inspect video for Chromecast compatibility")
def cmd(debug: bool=False):
    pass


@click.command(help="Generate ffmpeg conversion command.")
@click.argument("filename")
def get_cmd(filename: str):
    print(get_ffmpeg_cmd(filename))


@click.command(help="Convert video to Chromecast compatible encodings and container")
@click.argument("filename")
@click.option("-t", "--threads", default=THREADS,  type=click.INT,
              help="Count of threads for ffmpeg to use. Default: %s" % THREADS)
def convert(filename: str, threads: int):
    print(filename, "->", convert_video(filename, threads))


@click.command(help="Inspect video for transcoding options")
@click.argument("filename")
def inspect(filename: str):
    try:
        info = get_media_info(filename)

    except (FFProbeException, OSError) as e:
        print(e)
        return

    if need_to_transcode(info):
        transcode_str = ' '.join('%s: %s' % (k, v)
                                 for k, v in determine_transcodings(info).items())
        print("Transcode video to %s" % str(transcode_str))

    else:
        print("No need to transcode", filename)


@click.command(help="Watch directory and convert newly added videos")
@click.option('-i', '--ignore',
              help="File pattern to ignore. Flag can be used many times.",
              multiple=True)
@click.option("-d", "--debug", help="Print debug statements", is_flag=True, default=False)
@click.option("-t", "--threads", help="Number of threads to pass to ffmpeg", default=THREADS)
@click.argument("directory")
def watch(directory: str, ignore: tuple, debug: bool, threads: int):
    if ignore:
        print("Ignoring patterns:", ', '.join(ignore) + '...')

    watch_directory(directory, ignore_patterns=ignore, threads=threads, debug=debug)


@click.command(help="Print version information")
def version():
    print(__version__)


cmd.add_command(get_cmd)
cmd.add_command(convert)
cmd.add_command(inspect)
cmd.add_command(watch)
cmd.add_command(version)


if __name__ == "__main__":
    cmd()
