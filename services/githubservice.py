import os
import platform
import subprocess
import requests
import shutil
from sys import exit
from github import Github, GithubException
from tqdm import tqdm
from halo import Halo

from helpers.configfilehelper import get_config_key, reset_github_credentials,\
                                     GITHUB_SECTION, USER_KEY, PASS_KEY, GLOBAL_SECTION, GH_TOKEN
from helpers.colors import BOLD, CRITICAL,ENDC
from _version import __version__

ORGANIZATION = "Rankmi"


def get_github_instance():
    username = get_username()
    password = get_password()
    g = Github(username, password)
    try:
        return g.get_organization(ORGANIZATION)
    except GithubException as e:
        if e.status == 401:
            print('Tus credenciales de Github son incorrectas')
            reset_github_credentials()
            return get_github_instance()
        else:
            print(e)
            exit()


def start_development(priority, name):
    if priority in ['ShowStopper', 'Blocker', 'Critical']:
        version = input(CRITICAL + BOLD + "Determina la versión del Hotfix: " + ENDC)
        subprocess.run(['git', 'hf', 'hotfix', 'start', version])
    else:
        clean_name = "".join([char for char in name if char.isalnum() or char == "-"])
        subprocess.run(['git', 'hf', 'feature', 'start', clean_name])


def create_pr(compare):
    spinner = Halo(text="Creando Pull-Request", spinner="dots")
    org = get_github_instance()

    spinner.start()
    current_branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])[:-1].decode("utf-8")
    pr_title = "[" + current_branch[:8] + "] " + current_branch[9:].replace("-", " ")
    folder = os.getcwd().split("/")[-1]

    if is_folder_github_repo(folder):
        repo = org.get_repo(folder)
        try:
            pr_url = repo.create_pull(title=pr_title, body="", base=compare, head="Rankmi:" + current_branch).html_url
            spinner.succeed("Pull-Request creado. Puedes revisarlo en: " + pr_url)
            return pr_url
        except GithubException as e:
            spinner.fail(e)
            exit()
    
    else:
        spinner.fail("Para crear un Pull-Request debes localizarte en un repositorio válido.")


def create_release():
    token = 'token ' + get_token()
    last_release = get_last_release()

    spinner = Halo(text="Creating release for alfred", spinner="dots")
    spinner.start()

    if last_release['tag_name'] == __version__:
        spinner.info("There already is a release for version " + __version__)
        return last_release['upload_url'][:-13]

    response = requests.post(url="https://api.github.com/repos/Rankmi/alfred/releases",
                             json={"tag_name": __version__},
                             headers={'Authorization': token})

    if response.status_code == 201:
        spinner.succeed("Release created: v" + __version__)
        return response.json()['upload_url'][:-13]
    else:
        spinner.fail("Release creation failed")


def upload_asset(upload_url):
    token = 'token ' + get_token()
    file = open('dist/alfred', 'rb').read()

    spinner = Halo(text="Uploading asset to the corresponding release", spinner="dots")
    spinner.start()

    if platform.system() == "Darwin":
        name = {'name': 'alfred-for-mac'}
    elif platform.system() == "Linux":
        name = {'name': 'alfred-for-linux'}
    else:
        spinner.fail("You need to use a supported OS")
        exit()

    response = requests.post(upload_url,
                             headers={
                                 'Authorization': token,
                                 'Content-Type': 'application/octet-stream'
                             },
                             params=name,
                             data=file)

    if response.status_code == 201:
        spinner.succeed("Binary successfully uploaded")
        return response.json()['browser_download_url']
    else:
        spinner.fail(response)
        exit()


def download_last_release():
    assets = get_last_release()['assets']

    for asset in assets:
        if asset['name'] == 'alfred-for-mac' and platform.system() == "Darwin":
            asset_url = asset['url']
        elif asset['name'] == 'alfred-for-linux' and platform.system() == "Linux":
            asset_url = asset['url']

    file = requests.get(asset_url,
                        headers={
                            'Accept': 'application/octet-stream'
                        },
                        stream=True)

    with open("alfred", 'wb') as f:
        shutil.copyfileobj(file.raw, f)

    return True


def get_last_release():
    spinner = Halo()
    response = requests.get("https://api.github.com/repos/Rankmi/alfred/releases/latest")
    if response.status_code == 200:
        return response.json()
    else:
        spinner.fail(response.status_code)
        exit()


def update_binary():
    spinner = Halo(text="Updating alfred version", spinner="dots")
    spinner.start()

    if __version__ == get_last_release()['tag_name']:
        spinner.info("Your current alfred version is up-to-date")
        exit()

    spinner.text = "Downloading last binary realeased for", platform.system()
    download = download_last_release()

    if download:
        subprocess.run(["mv", "./alfred", "/usr/local/bin"])
        subprocess.run(["chmod", "+x", "/usr/local/bin/alfred"])
        spinner.succeed("alfred succesfully updated")
    else:
        spinner.fail("There was a problem downloading the file.")


def is_folder_github_repo(path=os.getcwd()):
    org = get_github_instance()
    repo_list = org.get_repos()
    
    return path.split("/")[-1] in [repo.name for repo in repo_list]


def get_username():
    username = get_config_key(GITHUB_SECTION, USER_KEY)
    if username:
        return username
    else:
        reset_github_credentials()
        return get_config_key(GITHUB_SECTION, USER_KEY)


def get_password():
    password = get_config_key(GITHUB_SECTION, PASS_KEY)
    if password:
        return password
    else:
        reset_github_credentials()
        return get_config_key(GITHUB_SECTION, PASS_KEY)


def get_token():
    token = get_config_key(GLOBAL_SECTION, GH_TOKEN)
    if token:
        return token
    else:
        reset_github_credentials()
        return get_config_key(GLOBAL_SECTION, GH_TOKEN)
