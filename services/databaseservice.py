import requests
from sys import exit
from http import HTTPStatus

from helpers.configfilehelper import get_config_key, reset_kato_credentials, KATO_SECTION, API_URL
from helpers.colors import print_msg, IconsEnum
from helpers.environmentclass import Environment
from services.youtrackservice import get_youtrack_user


def get_environments_list():
    username = get_verified_username()
    environments_url = get_kato_url() + f"/{username}/database"
    request = requests.get(environments_url)
    if request.ok and request.json():
        return [Environment.from_dict(env) for env in request.json()] 
    elif request.ok:
        print_msg(IconsEnum.INFO, "No tienes environments creados")
        exit()
    else:
        print_msg(IconsEnum.ERROR, "Hubo un error buscando los environments")
        return request.status_code


def get_environment(date):
    username = get_verified_username()
    environment_url = get_kato_url() + f"/{username}/database/{date}"
    request = requests.get(environment_url)
    if request.ok:
        return Environment.from_dict(request.json())
    elif request.status_code == HTTPStatus.NOT_FOUND:
        print_msg(IconsEnum.ERROR, "El environment indicado no existe")
        exit()
    else:
        print_msg(IconsEnum.ERROR, f"<{request.status_code}> No se pudo obtener información del environment solicitado")


def create_environment(date):
    username = get_verified_username()
    environment_url = get_kato_url() + f"/{username}/database/{date}"
    print_msg(IconsEnum.UNICORN, "Creando environment en Kato para %s" % date)
    request = requests.post(environment_url)
    if request.ok:
        print_msg(IconsEnum.SUCCESS, "El environment fue creado correctamente")
        return Environment.from_dict(request.json())
    elif request.status_code == HTTPStatus.FORBIDDEN:
        print_msg(IconsEnum.ERROR, "Has alcanzado el máximo de environment simultaneos.")
        return request.status_code
    elif request.status_code == HTTPStatus.NOT_FOUND:
        print_msg(IconsEnum.ERROR, "La imagen para el día indicado no existe.")
        return request.status_code
    else:
        print_msg(IconsEnum.ERROR, f"<{request.status_code}> Hubo un error realizando la solicitud")
        exit()


def delete_environment(date):
    username = get_verified_username()
    environment_url = get_kato_url() + f"/{username}/database/{date}"
    request = requests.delete(environment_url)
    if request.ok:
        print_msg(IconsEnum.SUCCESS, "El environment fue eliminado correctamente")
    elif request.status_code == HTTPStatus.NOT_FOUND:
        print_msg(IconsEnum.ERROR, "El environment indicado no existe")
    else:
        print_msg(IconsEnum.ERROR, "Hubo un error eliminando el environment")
        return request.status_code


def get_available_images():
    request_url = get_kato_url() + "/docker-images"
    request = requests.get(request_url)
    if request.ok:
        return request.json()
    else:
        print_msg(IconsEnum.ERROR, "Hubo un problema solicitando la lista de imagenes disponibles.")
        exit()


def get_kato_url():
    url = get_config_key(KATO_SECTION, API_URL)
    if url:
        return url
    else:
        print_msg(IconsEnum.ERROR, "No has ingresado tus credenciales para Kato")
        reset_kato_credentials()
        return get_config_key(KATO_SECTION, API_URL)


def get_verified_username():
    username = get_youtrack_user()
    if "@" in username:
        split_username = username.split("@")
        username = split_username[0]
    return username
