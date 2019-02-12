from github import Github

from configfilehelper import get_config_key, USER_KEY, GITHUB_SECTION, PASS_KEY, reset_github_credentials

ORGANIZATION = "Rankmi"


def create_repo(name) -> str:
    username = get_username()
    password = get_password()
    g = Github(username, password)
    org = g.get_organization(ORGANIZATION)
    print("Repositorio exitosamente creado en https://github.com/" + org.create_repo(name, private=True).full_name)


def create_branch(repository, base, name):
    username = get_username()
    password = get_password()
    g = Github(username, password)
    org = g.get_organization(ORGANIZATION)
    repo = org.get_repo(repository)
    source = repo.get_branch(base)
    repo.create_git_ref(ref='refs/heads/' + name, sha=source.commit.sha)
    print('Rama ' +repository+'/'+name+ ' creada exitosamente. Puedes verla en: https://github.com/Rankmi/'+repository+'/tree/'+name)


def create_pr(titulo, compare, rama, repository):
    username = get_username()
    password = get_password()
    g = Github(username, password)
    org = g.get_organization(ORGANIZATION)
    repo = org.get_repo(repository)
    print("Pull request creado. Puedes revisarlo en:", repo.create_pull(title=titulo, body="", base=compare, head="Rankmi:"+rama).html_url)


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
