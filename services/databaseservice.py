import requests
from sys import exit
from http import HTTPStatus

from helpers.configfilehelper import get_config_key, reset_kato_credentials, KATO_SECTION, USER_KEY, API_URL
from helpers.colors import print_msg, IconsEnum
from services.githubservice import get_username


def get_environments_list():
    username = get_username()
    environments_url = get_kato_url() + f"/{username}/database"
    request = requests.get(environments_url)
    if request.ok:
        return request
    elif request.status_code == HTTPStatus.NOT_FOUND:
        print_msg(IconsEnum.INFO, "No tienes environments creados")
        exit()
    else:
        print_msg(IconsEnum.ERROR, "Hubo un error buscando los environments")
        return request.status_code


def get_environment(date):
    username = get_username()
    environment_url = get_kato_url() + f"/{username}/database/{date}"
    request = requests.get(environment_url)
    if request.ok:
        return request
    elif request.status_code == HTTPStatus.NOT_FOUND:
        print_msg(IconsEnum.INFO, "El environment indicado no existe")
    else:
        print_msg(IconsEnum.ERROR, "No se pudo obtener información del environment solicitado")
        return request.status_code


def create_environment(date):
    username = get_username()
    environment_url = get_kato_url() + f"/{username}/database/{date}"
    print_msg(IconsEnum.UNICORN, "Creando environment en Kato para %s" % date)
    request = requests.post(environment_url)
    if request.ok:
        print_msg(IconsEnum.SUCCESS, "El environment fue creado correctamente")
        return request
    elif request.status_code == HTTPStatus.FORBIDDEN:
        print_msg(IconsEnum.ERROR, "Has alcanzado el máximo de environment simultaneos.")
        return request.status_code
    else:
        print_msg(IconsEnum.ERROR, "Hubo un error realizando la solicitud")
        return request.status_code


def delete_environment(date):
    username = get_username()
    environment_url = get_kato_url() + f"/{username}/database/{date}"
    request = requests.delete(environment_url)
    if request.ok:
        print_msg(IconsEnum.SUCCESS, "El environment fue eliminado correctamente")
        return request
    elif request.status_code == HTTPStatus.NOT_FOUND:
        print_msg(IconsEnum.ERROR, "El environment indicado no existe")
    else:
        print_msg(IconsEnum.ERROR, "Hubo un error eliminando el environment")
        return request.status_code


def get_kato_url():
    url = get_config_key(KATO_SECTION, API_URL)
    if url:
        return url
    else:
        print_msg(IconsEnum.ERROR, "No has ingresado tus credenciales para Kato")
        reset_kato_credentials()
        return get_config_key(KATO_SECTION, API_URL)
