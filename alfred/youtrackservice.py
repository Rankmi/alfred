import json

import requests

from .configfilehelper import get_config_key, YOUTRACK_SECTION, YOUTRACK_KEY, USER_KEY, \
    reset_youtrack_credentials

__base_url = "https://rankmi.myjetbrains.com/youtrack/api/"


def get_my_open_issues():
    params = dict(fields="project(shortName),numberInProject,summary",
                  query="for: " + get_youtrack_user() + " #unresolved")
    request_url = __base_url + "issues"
    user_request = requests.get(request_url, headers=get_header(), params=params)
    user_list = json.loads(user_request.text)
    for user in user_list:
        deserialized_user = User(user['summary'], user['numberInProject'], user['project'])
        print(deserialized_user)


def get_youtrack_user():
    y_user = get_config_key(YOUTRACK_SECTION, USER_KEY)
    if y_user is not None:
        return y_user
    else:
        print("No has ingresado tus credenciales de youtrack")
        reset_youtrack_credentials()
        return get_config_key(YOUTRACK_SECTION, USER_KEY)


def get_header():
    y_key = get_config_key(YOUTRACK_SECTION, YOUTRACK_KEY)
    if y_key is not None:
        return dict(Authorization=f"Bearer {y_key}")
    else:
        print("No has ingresado tus credenciales de youtrack")
        reset_youtrack_credentials()
        return get_config_key(YOUTRACK_SECTION, YOUTRACK_KEY)


class User:
    def __init__(self, summary, number_in_project, project):
        self.summary = summary
        self.numberInProject = number_in_project
        self.project = project

    def __str__(self):
        return str(f"{self.project['shortName']}-{self.numberInProject}-{str(self.summary).replace(' ', '_')}")
