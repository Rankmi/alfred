import os
import subprocess
from github import Github

from alfred.configfilehelper import get_config_key, USER_KEY, GITHUB_SECTION, PASS_KEY, reset_github_credentials

ORGANIZATION = "Rankmi"


def get_github_instance():
    username = get_username()
    password = get_password()
    return Github(username, password)


def create_repo(name) -> str:
    g = get_github_instance()
    org = g.get_organization(ORGANIZATION)
    print("Repositorio creado exitosamente en https://github.com/" + org.create_repo(name, private=True).full_name)


def create_branch(repository, base, name):
    g = get_github_instance()
    org = g.get_organization(ORGANIZATION)
    repo = org.get_repo(repository)
    source = repo.get_branch(base)
    repo.create_git_ref(ref='refs/heads/' + name, sha=source.commit.sha)
    print(
        'Rama ' + repository + '/' + name + ' creada exitosamente. Puedes verla en: https://github.com/Rankmi/' + repository + '/tree/' + name)


def create_pr(compare):
    g = get_github_instance()
    org = g.get_organization(ORGANIZATION)
    
    rama = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])[:-1].decode("utf-8")
    titulo = "[" + rama.split('/')[0] +  "] " + rama.split('/')[1].replace("-", " ")
    folder = os.getcwd().split("/")[-1]

    if is_folder_github_repo(folder):
        repo = org.get_repo(folder)
        print("Pull request creado. Puedes revisarlo en:",
              repo.create_pull(title=titulo, body="", base=compare, head="Rankmi:" + rama).html_url)
    
    else:
        print("Para crear un Pull request debes localizarte en un repositorio válido.")
        

def is_folder_github_repo(path=os.getcwd()):
    g = get_github_instance()
    org = g.get_organization(ORGANIZATION)
    repoList = org.get_repos()
    
    return path.split("/")[-1] in [repo.name for repo in repoList]


def get_username():
    username = get_config_key(GITHUB_SECTION, USER_KEY)
    if username is not None:
        return username
    else:
        reset_github_credentials()
        return get_config_key(GITHUB_SECTION, USER_KEY)


def get_password():
    password = get_config_key(GITHUB_SECTION, PASS_KEY)
    if password is not None:
        return password
    else:
        reset_github_credentials()
        return get_config_key(GITHUB_SECTION, PASS_KEY)
