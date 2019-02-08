from github import Github

from configfilehelper import get_config_key, USER_KEY, GITHUB_SECTION, PASS_KEY, reset_github_credentials

ORGANIZATION = "Rankmi"


def create_repo(name) -> str:
    username = get_config_key(GITHUB_SECTION, USER_KEY)
    password = get_config_key(GITHUB_SECTION, PASS_KEY)
    if username is not None and password is not None:
        g = Github(get_username(), get_password())
        org = g.get_organization(ORGANIZATION)
        print(org.create_repo(name).full_name)
    else:
        print("No has configurado tus credenciales de Github")
        reset_github_credentials()


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
