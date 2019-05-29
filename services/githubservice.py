import os
import platform
import subprocess
import requests
import shutil
from sys import exit
from github import Github, GithubException

from helpers.configfilehelper import get_config_key, reset_github_credentials,\
                                     GITHUB_SECTION, USER_KEY, PASS_KEY, GLOBAL_SECTION, GH_TOKEN
from services.youtrackservice import get_issue_by_id
from helpers.colors import print_msg, IconsEnum
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


def hubflow_interaction(action, type, name, hf=False):
    if not is_folder_hf_initialized():
        print_msg(IconsEnum.INFO, "Configurando Hubflow correctamente")
        config_hf_repo()

    if hf:
        subprocess.run(['git', 'hf', 'update'])
        if 'hotfix/' in '-'.join(get_created_branches()):
            subprocess.run(['git', 'checkout', '-b', 'hotfix/' + name])
            subprocess.run(['git', 'push', '--set-upstream', 'origin', 'hotfix/' + name])
            return

    if action == "start":
        hf_output = subprocess.run(['git', 'hf', type, 'start', name])
        if hf_output.returncode:
            print_msg(IconsEnum.ERROR, 'Hubo un error creando la rama')
            exit()
    elif action == "finish":
        hf_output = subprocess.run(['git', 'hf', type, 'finish', name])
        if hf_output.returncode:
            print_msg(IconsEnum.ERROR, 'Hubo un error finalizando la tarea')
            exit()


def is_folder_hf_initialized():
    branches_config = []
    for branch in ["master", "develop"]:
        branch_value = subprocess.run(['git', 'config', 'hubflow.branch.' + branch], stdout=subprocess.PIPE)
        branches_config.append(branch_value.stdout.decode('utf-8').strip())

    prefixes_config = []
    for prefix in ["feature", "release", "hotfix", "support", "versiontag"]:
        prefix_value = subprocess.run(['git', 'config', 'hubflow.prefix.' + prefix], stdout=subprocess.PIPE)
        prefixes_config.append(prefix_value.stdout.decode('utf-8').strip())

    return branches_config == ["master", "development"] and prefixes_config == ["feature/", "release/", "hotfix/", "support/", ""] 


def config_hf_repo():
    hubflow_config = {
            'branch.master': 'master',
            'branch.develop': 'development',
            'prefix.feature': 'feature/',
            'prefix.release': 'release/',
            'prefix.hotfix': 'hotfix/',
            'prefix.support': 'support/',
            'prefix.versiontag': ''
    }
    
    for key, value in hubflow_config.items():
        subprocess.run(['git', 'config', 'hubflow.' + key, value])


def get_created_branches():
    return subprocess.run(['git', 'branch', '-a'], stdout=subprocess.PIPE).stdout.decode('utf-8').split()


def create_pr(compare, issue):
    org = get_github_instance()

    print_msg(IconsEnum.INFO, 'Creando Pull-Request')
    current_branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])[:-1].decode("utf-8")
    pr_title = "[" + issue.type + "] " + issue.id
    folder = os.getcwd().split("/")[-1]

    if is_folder_github_repo(folder):
        repo = org.get_repo(folder)
        try:
            pr_url = repo.create_pull(title=pr_title, body="", base=compare, head="Rankmi:" + current_branch).html_url
            print_msg(IconsEnum.SUCCESS, "Pull-Request creado. Puedes revisarlo en: " + pr_url)
            return pr_url
        except GithubException as e:
            print_msg(IconsEnum.ERROR, e)
            exit()
    else:
        print_msg(IconsEnum.ERROR, "Para crear un Pull-Request debes localizarte en un repositorio válido.")


def create_release():
    token = 'token ' + get_token()
    last_release = get_last_release()

    print_msg(IconsEnum.INFO, 'Creating release for alfred')

    if last_release['tag_name'] == __version__:
        print_msg(IconsEnum.INFO, "There already is a release for version " + __version__)
        return last_release['upload_url'][:-13]

    response = requests.post(url="https://api.github.com/repos/Rankmi/alfred/releases",
                             json={"tag_name": __version__},
                             headers={'Authorization': token})

    if response.status_code == 201:
        print_msg(IconsEnum.SUCCESS, "Release created: v" + __version__)
        return response.json()['upload_url'][:-13]
    else:
        print_msg(IconsEnum.ERROR, "Release creation failed")


def upload_asset(upload_url):
    token = 'token ' + get_token()
    file = open('dist/alfred', 'rb').read()

    print_msg(IconsEnum.INFO, "Uploading asset to the corresponding release")

    if platform.system() == "Darwin":
        name = {'name': 'alfred-for-mac'}
    elif platform.system() == "Linux":
        name = {'name': 'alfred-for-linux'}
    else:
        print_msg(IconsEnum.INFO, "You need to use a supported OS")
        exit()

    response = requests.post(upload_url,
                             headers={
                                 'Authorization': token,
                                 'Content-Type': 'application/octet-stream'
                             },
                             params=name,
                             data=file)

    if response.status_code == 201:
        print_msg(IconsEnum.SUCCESS, "Binary successfully uploaded")
        return response.json()['browser_download_url']
    else:
        print_msg(IconsEnum.ERROR, response)
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
    response = requests.get("https://api.github.com/repos/Rankmi/alfred/releases/latest")
    if response.status_code == 200:
        return response.json()
    else:
        print_msg(IconsEnum.ERROR, response.status_code)
        exit()


def update_binary():
    print_msg(IconsEnum.INFO, "Updating alfred version")

    if __version__ == get_last_release()['tag_name']:
        print_msg(IconsEnum.INFO, "Your current alfred version is up-to-date")
        exit()

    print_msg(IconsEnum.INFO, "Downloading last binary realeased for" + platform.system())
    download = download_last_release()

    if download:
        subprocess.run(["mv", "./alfred", "/usr/local/bin"])
        subprocess.run(["chmod", "+x", "/usr/local/bin/alfred"])
        print_msg(IconsEnum.SUCCESS, "alfred succesfully updated")
    else:
        print_msg(IconsEnum.ERROR, "There was a problem downloading the file.")


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
