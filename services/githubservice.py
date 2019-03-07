import os
import subprocess
from github import Github, GithubException

from alfred.configfilehelper import get_config_key, USER_KEY, GITHUB_SECTION, PASS_KEY, reset_github_credentials

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
            print(
            'Rama ' + name + ' creada exitosamente. Puedes verla en: https://github.com/Rankmi/' + folder + '/tree/' + name)
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


def create_pr(compare):
    org = get_github_instance()
    
    currentBranch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])[:-1].decode("utf-8")
    prTitle = "[" + currentBranch[:8] +  "] " + currentBranch[9:].replace("-", " ")
    folder = os.getcwd().split("/")[-1]

    if is_folder_github_repo(folder):
        repo = org.get_repo(folder)
        try:
            prUrl = repo.create_pull(title=prTitle, body="", base=compare, head="Rankmi:" + currentBranch).html_url
            print("Pull request creado. Puedes revisarlo en:", prUrl)
            return prUrl
        except GithubException as e:
            print(e)
            exit()
    
    else:
        print("Para crear un Pull request debes localizarte en un repositorio válido.")
        

def is_folder_github_repo(path=os.getcwd()):
    org = get_github_instance()
    repoList = org.get_repos()
    
    return path.split("/")[-1] in [repo.name for repo in repoList]


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

# def validate_credentials():
