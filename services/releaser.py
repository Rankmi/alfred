import platform
import subprocess

from helpers.colors import print_msg, IconsEnum
from helpers.configfilehelper import get_config_key, reset_github_credentials, RELEASER_SECTION, API_URL


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
    token = get_config_key(RELEASER_SECTION, API_URL)
    if token:
        return token
    else:
        print_msg(IconsEnum.ERROR, "No has ingresado tus credenciales de Github")
        reset_github_credentials()
        return get_config_key(RELEASER_SECTION, API_URL)
