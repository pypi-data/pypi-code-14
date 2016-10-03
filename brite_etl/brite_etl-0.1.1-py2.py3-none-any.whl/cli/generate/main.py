import click
import pkg_resources

from .frame import generate_frame, regenerate_all_frames


@click.group(help="Generate new calculations/frames")
def generate():
    """
        Kind of janky, but let's detect if brite_etl is installed as a package and warn them if it is.
    """
    if (pkg_resources.get_distribution('click').location == pkg_resources.get_distribution('brite_etl').location):
        click.secho('----------', fg='yellow')
        click.secho('HEY! Looks like you might be using brite_etl installed as a package. To generate new files, ' +
                    'you\'ll probably want to clone the repo and install using `python setup.py develop` instead.',
                    fg='yellow'
                    )
        click.echo()
        click.secho('Do you want to continue anyways? [y/n] ', nl=False, fg='yellow')
        c = click.getchar()
        click.echo()
        if c == 'y':
            click.secho('Moving on...', fg='green')
        elif c == 'n':
            click.secho('Aborting...', fg='red')
            exit()
        else:
            click.secho('Invalid Input', fg='red')
            exit()
    pass


generate.add_command(generate_frame)
generate.add_command(regenerate_all_frames)
