#!/usr/bin/env python3
"""alfred is your friend, alfred is your god, alfred is nothing
"""

import click
from _version import __version__
from helpers.configfilehelper import reset_credentials
from helpers.issueupdater import update_issue
from helpers.printer import print_issue, print_issue_list
from services.awsservice import get_backup, dumpbackup
from services.youtrackservice import get_issues_by_state, get_issue_by_id
from services.githubservice import create_release, upload_asset, download_last_release, update_binary
from services.releaser import release_alfred


@click.group(invoke_without_command=True)
@click.option('--version', '-v', is_flag=True)
def greet(version):
    if version:
        click.echo("alfred v" + __version__)


@greet.command()
@click.option('--out', '-o', type=click.Path())
@click.option('--extract', is_flag=True)
@click.option('--delete', is_flag=True)
@click.argument('database_date')
def get(database_date, out, extract, delete):
    get_backup(database_date, out, extract, delete)


@greet.command()
@click.argument("interface")
def reset(interface):
    reset_credentials(interface)


@greet.command()
@click.argument("action")
def release(action):
    if action == "new":
        upload_asset(create_release())
    elif action == "download":
        download_last_release()
    elif action[0] == "v":
        release_alfred(action[1:])


@greet.command()
def update():
    update_binary()


@greet.command()
@click.argument("state")
def tasks(state):
    print_issue_list(get_issues_by_state(state))


@greet.command()
@click.argument("action")
def task(action):
    update_issue(action)


@greet.command()
@click.argument('issue')
def issue(issue):
    print_issue(get_issue_by_id(issue))


@greet.command()
@click.argument('environment')
def dump(environment):
    dumpbackup(environment)


if __name__ == '__main__':
    greet(prog_name='alfred.sh')
