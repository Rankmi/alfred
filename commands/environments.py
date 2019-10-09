from http import HTTPStatus

import click

from helpers.printer import print_envs_list, print_available_images, print_env
from services.databaseservice import get_environments_list, get_available_images, create_environment, \
    delete_environment, get_environment, restart_environment


@click.group(name='env', help='Interactions with Kato Databases Service')
def environment():
    pass


@environment.command(name='list', help='Show all the environments created for the user')
def list_envs():
    environments = get_environments_list()
    print_envs_list(environments)


@environment.command(name='images', help='List available dates for requesting environments')
def list_available_images():
    available_images = get_available_images()
    print_available_images(available_images)


@environment.command(name='new', help='Creates an environment for a given date (YYYY_MM_DD)')
@click.argument('date')
def new_env(date: str):
    env = create_environment(date)
    if env == HTTPStatus.FORBIDDEN:
        print_envs_list(get_environments_list())
        delete_environment(input("¿Qué fecha deseas eliminar?: "))
    elif env == HTTPStatus.NOT_FOUND:
        available_images = get_available_images()
        print_available_images(available_images, 5)
    else:
        print_env(env)


@environment.command(name='get', help="Prints an environment's information from the given date (YYYY_MM_DD)")
@click.argument('date')
def get_env(date: str):
    env = get_environment(date)
    print_env(env)


@environment.command(name='del', help='Deletes the environment associated to a date (YYYY_MM_DD)')
@click.argument('date')
def delete_env(date: str):
    delete_environment(date)


@environment.command(name='rt', help='Restarts the environment for the given date (YYYY_MM_DD)')
def restart_env(date: str):
    restart_environment(date)
