import os
import platform
import subprocess
import requests
import shutil
from sys import exit
from github import Github, GithubException
from tqdm import tqdm

from helpers.configfilehelper import get_config_key, reset_github_credentials,\
                                     GITHUB_SECTION, USER_KEY, PASS_KEY, GH_TOKEN
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


def create_branch(base, name):
    org = get_github_instance()

    if is_folder_github_repo():
        folder = os.getcwd().split("/")[-1]
        repo = org.get_repo(folder)
        source = repo.get_branch(base)

        try:
            repo.create_git_ref(ref='refs/heads/' + name, sha=source.commit.sha)
            print('Rama ' + name + ' creada exitosamente. Puedes verla en: '
                                   'https://github.com/Rankmi/' + folder + '/tree/' + name)

        except GithubException as e:
            if e.status == 422:
                print('La rama para esta tarea ya existe')
            else:
                print(e)
                exit()

        subprocess.run(["git", "fetch", "--all"])
        subprocess.run(["git", "checkout", name])

    else:
        print("Debes localizarte en un repositorio válido.")


def delete_branch(branch):
    org = get_github_instance()
    folder = os.getcwd().split("/")[-1]
    repo = org.get_repo(folder)
    repo.get_git_ref(ref='heads/' + branch).delete()
    subprocess.run(["git", "checkout", "development"])
    subprocess.run(["git", "branch", "-D", branch])
    subprocess.run(["git", "pull"])


def create_pr(compare):
    org = get_github_instance()
    
    current_branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])[:-1].decode("utf-8")
    pr_title = "[" + current_branch[:8] + "] " + current_branch[9:].replace("-", " ")
    folder = os.getcwd().split("/")[-1]

    if is_folder_github_repo(folder):
        repo = org.get_repo(folder)
        try:
            pr_url = repo.create_pull(title=pr_title, body="", base=compare, head="Rankmi:" + current_branch).html_url
            print("Pull request creado. Puedes revisarlo en:", pr_url)
            return pr_url
        except GithubException as e:
            print(e)
            exit()
    
    else:
        print("Para crear un Pull request debes localizarte en un repositorio válido.")


def create_release():
    token = 'token ' + get_token()
    last_release = get_last_release()

    if last_release['tag_name'] == __version__:
        print("There already is a release for version " + __version__)
        return last_release['upload_url'][:-13]

    response = requests.post(url="https://api.github.com/repos/Rankmi/alfred/releases",
                             json={"tag_name": __version__},
                             headers={'Authorization': token})

    print("Release created: v" + __version__)
    return response.json()['upload_url'][:-13]


def upload_asset(upload_url):
    token = 'token ' + get_token()
    file = open('dist/alfred', 'rb').read()

    if platform.system() == "Darwin":
        name = {'name': 'alfred-for-mac'}
    elif platform.system() == "Linux":
        name = {'name': 'alfred-for-linux'}
    else:
        return "You need to use a supported OS."

    response = requests.post(upload_url,
                             headers={
                                 'Authorization': token,
                                 'Content-Type': 'application/octet-stream'
                             },
                             params=name,
                             data=file)

    if response.status_code == 201:
        print("Binary successfully uploaded")
        return response.json()['browser_download_url']
    else:
        return response.status_code


def download_last_release():
    token = 'token ' + get_token()

    last_release = str(get_last_release()['id'])

    asset = requests.get('https://api.github.com/repos/Rankmi/alfred/releases/' + last_release,
                         headers={
                             'Authorization': token
                         })

    for asset in asset.json()['assets']:
        if asset['name'] == 'alfred-for-mac' and platform.system() == "Darwin":
            asset_url = asset['url']
        elif asset['name'] == 'alfred-for-linux' and platform.system() == "Linux":
            asset_url = asset['url']

    file = requests.get(asset_url,
                        headers={
                            'Authorization': token,
                            'Accept': 'application/octet-stream'
                        },
                        stream=True)


    with open("alfred", 'wb') as f:
        shutil.copyfileobj(file.raw, f)

    return "alfred"


def update_binary():
    if __version__ == get_last_release()['tag_name']:
        return "Your alfred version is up-to-date"

    print("Downloading last binary realeased for " + platform.system())
    download_last_release()

    subprocess.run(["mv", "./alfred", "/usr/local/bin"])
    return "alfred succesfully updated"


def get_last_release():
    token = 'token ' + get_token()

    response = requests.get("https://api.github.com/repos/Rankmi/alfred/releases",
                            headers={
                                'Authorization': token
                            })

    return response.json()[0]


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
    token = get_config_key(GITHUB_SECTION, GH_TOKEN)
    if token:
        return token
    else:
        reset_github_credentials()
        return get_config_key(GITHUB_SECTION, GH_TOKEN)
