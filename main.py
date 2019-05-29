#!/usr/bin/env python3
"""alfred is your friend, alfred is your god, alfred is nothing
"""

import click
from sys import exit
from _version import __version__
from helpers.configfilehelper import reset_credentials
from helpers.issueupdater import update_issue, finish_issue, STATES
from helpers.printer import print_issue, print_issue_list
from services.awsservice import get_backup, dumpbackup
from services.youtrackservice import get_issues_by_state, get_issue_by_id, execute_command
from services.githubservice import create_release, upload_asset, download_last_release, update_binary, \
    is_folder_github_repo, hubflow_interaction
from services.releaser import release_alfred
from helpers.colors import BOLD, HEADER, ENDC, print_msg, GREEN, CRITICAL, IconsEnum


@click.group(invoke_without_command=True)
@click.option('--version', '-v', is_flag=True)
def greet(version):
    if version:
        print_msg(IconsEnum.UNICORN, HEADER + "alfred" + ENDC + BOLD + " v" + __version__)


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
    if is_folder_github_repo():
        update_issue(action)
    else:
        print_msg(IconsEnum.ERROR, 'Debes localizarte en un repositorio válido')
        exit()


@greet.command()
@click.argument('type')
@click.argument('name')
def start(type, name):
    if not is_folder_github_repo():
        print_msg(IconsEnum.ERROR, 'Debes localizarte en un repositorio válido')
        exit()

    if type == 'hotfix':
        hubflow_interaction('start', type, name, hf=True)
        name = 'RKM-' + name.split('.')[2]
    else:
        hubflow_interaction('start', type, name)

    execute_command(get_issue_by_id(name), "State", STATES["prog"])
    print_msg(IconsEnum.SUCCESS, "Estado de la tarea fue cambiado a 'En progreso'")


@greet.command()
@click.argument('type')
@click.argument('name')
def submit(type, name):
    if not is_folder_github_repo():
        print_msg(IconsEnum.ERROR, 'Debes localizarte en un repositorio válido')
        exit()

    if type == 'hotfix':
        name = name.split('.')[2]

    finish_issue(name)


@greet.command()
@click.argument('type')
@click.argument('name')
def finish(type, name):
    if not is_folder_github_repo():
        print_msg(IconsEnum.ERROR, 'Debes localizarte en un repositorio válido')
        exit()

    hubflow_interaction('finish', type, name)

    if type == 'hotfix':
        name = name.split('.')[2]
        execute_command(get_issue_by_id(name), "State", STATES["production"])
        print_msg(IconsEnum.SUCCESS, "Estado de la tarea fue cambiado a " + GREEN + "'Producción'")
    else:
        execute_command(get_issue_by_id(name), "State", STATES["accepted"])
        print_msg(IconsEnum.SUCCESS, "Estado de la tarea fue cambiado a " + GREEN + "'Aceptado'")


@greet.command()
@click.argument('issue')
def issue(issue):
    print_issue(get_issue_by_id(issue))


@greet.command()
@click.argument('environment')
def dump(environment):
    dumpbackup(environment)


if __name__ == '__main__':
    greet(prog_name='alfred')
