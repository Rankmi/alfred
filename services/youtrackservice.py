# -*- coding: utf-8 -*-
import json
import requests
from sys import exit

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
    "list": "#Unresolved"
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
        print("Error:", user_request.status_code, "on get_issues_by_state")
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
        print("Error:", user_request.status_code, "on get_issue_by_id")
        exit()


def execute_command(issue, field, value):
    request_url = "https://rankmi.myjetbrains.com/youtrack/rest/issue/" + issue.id + "/execute?command=" + field + "+" + value
    user_request = requests.post(request_url, headers=get_header())

    if user_request.ok:
        return user_request
    else:
        print("Error:", user_request.status_code, "on execute_command")
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
    if y_key:
        return dict(Authorization=f"Bearer {y_key}")
    else:
        print("No has ingresado tus credenciales de youtrack")
        reset_youtrack_credentials()
        return get_config_key(YOUTRACK_SECTION, YOUTRACK_KEY)
