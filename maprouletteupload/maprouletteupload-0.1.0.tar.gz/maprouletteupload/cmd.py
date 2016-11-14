import click
import json
import webbrowser

from .api import DIFFICULTIES, create_challenge, get_challenge, upload_tasks
from .tasks import create_tasks


@click.command()
@click.option('--api-key', help='Your API key, via Maproulette.')
@click.option('--challenge-id', type=int,
        help='The challenge ID these tasks should be added to.')
@click.option('--identifier', type=str, default='identifier',
        help=('The name of the property to use as the identifier. Default: '
            '"identifier".'))
@click.option('--instruction', type=str, default='instruction',
        help=('The name of the property to use as the instruction. Default: '
            '"instruction".'))
@click.option('--name', type=str, default='name',
        help=('The name of the property to use as the name. Default: "name".'))
@click.option('--geojson-file', type=click.Path(exists=True),
        help=('A GeoJSON file of tasks to upload. Alternatively, you can '
            'provide this file via stdin.'))
@click.version_option()
def upload(api_key, challenge_id, identifier, instruction, name, geojson_file):
    """Upload a GeoJSON file (or stdin) of tasks to Maproulette."""
    try:
        if not api_key:
            raise click.BadParameter('API key required. Please try again.')
        if geojson_file:
            geojson = json.load(open(geojson_file, 'r'))
        else:
            geojson = json.load(click.get_text_stream('stdin'))

        challenge = get_challenge(challenge_id)
        if challenge is None:
            challenge = prompt_and_create_challenge(api_key)
            challenge_id = challenge['id']
            click.echo('Challenge with id %s created' % challenge['id'])

        create_tasks_kwargs = {
            'identifier_field': identifier,
            'instruction_field': instruction,
            'name_field': name,
        }

        tasks = list(create_tasks(geojson, **create_tasks_kwargs))
        response = upload_tasks(api_key, challenge_id, tasks)
        click.echo('Done uploading tasks. Status code: %d' % response.status_code)
        click.echo(response.text)

        if click.confirm('Start challenge now?'):
            webbrowser.open('http://maproulette.org/map/%d' % challenge_id)
    except Exception as e:
        click.echo(e)


def prompt_and_create_challenge(api_key):
    if click.confirm('Challenge does not exist. Create one now?'):
        name = click.prompt('Please enter a name', type=str)
        instruction = click.prompt('Please enter a default instruction', type=str)
        difficulty = click.prompt('Please enter a difficulty. [e]asy, [n]ormal, or e[x]pert', type=str)
        challenge = create_challenge(api_key, name=name,
                instruction=instruction, difficulty=DIFFICULTIES[difficulty])
        return challenge


if __name__ == '__main__':
    upload()
