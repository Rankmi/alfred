import click

from services.githubservice import upload_asset, create_release
from services.releaser import release_alfred


@click.group(name='dev', help='For Alfred development')
def development():
    pass


@development.command()
@click.argument("action")
def release(action):
    if action == "new":
        upload_asset(create_release())
    elif action[0] == "v":
        release_alfred(action[1:])
