import click

from helpers.colors import print_msg, IconsEnum, GREEN
from helpers.issueupdater import STATES, finish_issue
from services.githubservice import is_folder_github_repo, hubflow_interaction
from services.youtrackservice import execute_command, get_issue_by_id


@click.group(name='flow', help='Commands for Hubflow work')
def hubflow():
    pass


@click.group()
def start():
    pass


@click.group()
def submit():
    pass


@click.group()
def finish():
    pass


hubflow.add_command(start)


@start.command(name='ft')
@click.argument('name')
def feature(name):
    if not is_folder_github_repo():
        print_msg(IconsEnum.ERROR, 'Debes localizarte en un repositorio válido')
        exit()

    hubflow_interaction('start', 'feature', name)
    execute_command(get_issue_by_id(name), "State", STATES["prog"])
    print_msg(IconsEnum.SUCCESS, "Estado de la tarea fue cambiado a 'En progreso'")


@start.command(name='hf')
@click.argument('name')
def hotfix(name):
    if not is_folder_github_repo():
        print_msg(IconsEnum.ERROR, 'Debes localizarte en un repositorio válido')
        exit()

    hubflow_interaction('start', 'hotfix', name, hf=True)
    name = 'RKM-' + name.split('.')[2]
    execute_command(get_issue_by_id(name), "State", STATES["prog"])
    print_msg(IconsEnum.SUCCESS, "Estado de la tarea fue cambiado a 'En progreso'")


hubflow.add_command(submit)


@submit.command(name='ft')
@click.argument('name')
def feature(name):
    if not is_folder_github_repo():
        print_msg(IconsEnum.ERROR, 'Debes localizarte en un repositorio válido')
        exit()

    finish_issue(name)


@submit.command(name='hf')
@click.argument('name')
def hotfix(name):
    if not is_folder_github_repo():
        print_msg(IconsEnum.ERROR, 'Debes localizarte en un repositorio válido')
        exit()

    name = name.split('.')[2]
    finish_issue(name)


hubflow.add_command(finish)


@finish.command(name='ft')
@click.argument('name')
def feature(name):
    if not is_folder_github_repo():
        print_msg(IconsEnum.ERROR, 'Debes localizarte en un repositorio válido')
        exit()

    hubflow_interaction('finish', 'feature', name)
    execute_command(get_issue_by_id(name), "State", STATES["accepted"])
    print_msg(IconsEnum.SUCCESS, "Estado de la tarea fue cambiado a " + GREEN + "'Aceptado'")


@finish.command(name='hf')
@click.argument('name')
def hotfix(name):
    if not is_folder_github_repo():
        print_msg(IconsEnum.ERROR, 'Debes localizarte en un repositorio válido')
        exit()

    hubflow_interaction('finish', 'hotfix', name)
    name = name.split('.')[2]
    execute_command(get_issue_by_id(name), "State", STATES["production"])
    print_msg(IconsEnum.SUCCESS, "Estado de la tarea fue cambiado a " + GREEN + "'Producción'")
