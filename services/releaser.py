import platform
import subprocess

from data.Releaser import ReleaseRankmiResponse, ReleaseProjectResponse
from helpers.colors import print_msg, IconsEnum
from helpers.configfilehelper import get_config_key, reset_github_credentials, RELEASER_SECTION, API_URL


def rel_rankmi_response(response: ReleaseRankmiResponse):
    if response.ok:
        print_msg(IconsEnum.UNICORN, "Release realizado correctamente")
    elif not response.ok:
        print_msg(IconsEnum.ERROR, "Hubo un error realizando el Release")
        print_msg(IconsEnum.INFO, response.status)
    print_msg(IconsEnum.INFO, response.api_message)
    print_msg(IconsEnum.INFO, response.app_message)


def rel_project_response(response: ReleaseProjectResponse):
    if response.ok:
        print_msg(IconsEnum.UNICORN, "Release realizado correctamente")
    elif not response.ok:
        print_msg(IconsEnum.ERROR, "Hubo un error realizando el Release")
        print_msg(IconsEnum.INFO, response.status)
    print_msg(IconsEnum.INFO, response.message)


def release_alfred(version):
    if platform.system() != "Darwin":
        print("You need to release alfred from a Mac machine.")
        return 403

    with open("_version.py", "w") as f:
        f.write("__version__ = '" + version + "'\n")

    print("Releasing binary for Mac systems.")
    subprocess.run(["./generator.sh", "ins", "gen"])
    subprocess.run(["./dist/alfred", "release", "new"])

    print("Releasing binary for Linux systems.")
    subprocess.call("cp ~/.alfred.conf .", shell=True)
    subprocess.run(["docker", "build", "-t", "alfredock:"+version, "."])
    subprocess.run(["rm", ".alfred.conf"])

    print("All binaries successfully uploaded.")
    return 201


def get_releaser_url():
    url = get_config_key(RELEASER_SECTION, API_URL)
    if url:
        return url
    else:
        print_msg(IconsEnum.ERROR, "No has ingresado tus credenciales de Github")
        reset_github_credentials()
        return get_config_key(RELEASER_SECTION, API_URL)
