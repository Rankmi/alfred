import click

from _version import __version__
from commands.database import database
from commands.environments import environment
from commands.hubflow import hubflow
from commands.development import development
from commands.issues import issues
from commands.release import release
from commands.reset import reset
from services.githubservice import update_binary

ALFRED_VERSION = f"version {__version__}"


@click.group(help=ALFRED_VERSION)
def greet():
    pass


@greet.command(help="Updates Alfred binary to the latest version")
def update():
    update_binary()


greet.add_command(database)
greet.add_command(development)
greet.add_command(environment)
greet.add_command(hubflow)
greet.add_command(issues)
greet.add_command(release)
greet.add_command(reset)

if __name__ == '__main__':
    greet(prog_name="alfred")
