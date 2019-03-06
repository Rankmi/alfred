# -*- coding: utf-8 -*-
import json
import requests

from alfred.configfilehelper import get_config_key, YOUTRACK_SECTION, YOUTRACK_KEY, USER_KEY, \
    reset_youtrack_credentials
from services.issueclasses import Issue, Context, Assignees

__base_url = "https://rankmi.myjetbrains.com/youtrack/api/"

STATES = {
    "todo": "#{Por hacer}",
    "prog": "#{En progreso}",
    "cr": "#{Para CodeReview}",
    "changes": "#{CR Cambios Solicitados}",
    "qa": "#{Pendiente de QA}",
    "review": "#{En Review}",
    "accepted": "#{Aceptado}",
    "rejected": "#{Rechazado}",
    "open": "#Unresolved"
}


def get_issues_by_state(state):
    params = dict(fields="project(shortName),numberInProject,summary,"
                         "fields(projectCustomField(field(name)),value(name))",
                  query=get_youtrack_user() + " " + STATES[state])

    request_url = __base_url + "issues"
    user_request = requests.get(request_url, headers=get_header(), params=params)
    user_list = json.loads(user_request.text)
    if user_request.ok:
        issues = [Issue(issue) for issue in user_list if Issue(issue).state not in ["Archivado", "Backlog"]]
        return issues
    else:
        print("Error:", user_request.status_code)
        exit()


def get_issue_by_id(id):
    params = dict(fields="description,created,numberInProject,project(shortName),summary,reporter(name),"
                         "fields(projectCustomField(field(name)),value(name))")
    if id.isdigit():
        request_url = __base_url + "issues/RKM-" + id
    else:
        request_url = __base_url + "issues/" + id
    user_request = requests.get(request_url, headers=get_header(), params=params)
    if user_request.ok:
        fields = json.loads(user_request.text)
        return Issue(fields, complete=True)
    else:
        print("Error:", user_request.status_code)
        exit()


def change_issue_state(id, state):
    if id.isdigit():
        request_url = "https://rankmi.myjetbrains.com/youtrack/rest/issue/RKM-" + id + "/execute?command=State+" + state
    else:
        request_url = "https://rankmi.myjetbrains.com/youtrack/rest/issue/" + id + "/execute?command=State+" + state

    response = requests.post(request_url, headers=get_header())
    if response.ok:
        return response
    else:
        print("Error:", response.status_code)
        exit()


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
