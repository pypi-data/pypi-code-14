import click
import os

@click.group()
def cli():
    pass

@cli.command()
@click.argument('filepath', type=click.Path(exists=True))
@click.option('--no-input', is_flag=True)
def create(filepath, no_input):

    name= 'rinobot-plugin'
    author= ''
    description= ''
    repo=''

    if os.path.isdir(filepath):
        return click.echo('The directory `%s` already exists. Aborting.' % filepath)

    if not no_input:
        name= click.prompt('Name of the plugin')
        author= click.prompt('Author', default=os.environ.get('USER', ''))
        description= click.prompt('Package description', default=None)
        repo= click.prompt('Package git repository (if it exists)', default=None)

        click.echo('\n\tPlugin name: %s' % name)
        click.echo('\tAuthor: %s' % author)
        click.echo('\tDescription: %s' % description)
        click.echo('\tGit repo: %s\n\n' % repo)

        click.confirm('Do you want to continue?', abort=True)

    os.mkdir(filepath)

    
