#!/usr/bin/env python3
"""alfred is your friend, alfred is your god, alfred is nothing
"""

import click

from alfred.configfilehelper import config_file_exists, reset_credentials
from alfred.issueupdater import update_issue
from alfred.printer import print_issue, print_issue_list
from services.awsservice import get_backup, dumpbackup
from services.youtrackservice import get_issues_by_state, get_issue_by_id


@click.group()
def greet():
    pass


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
