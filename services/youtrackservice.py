# -*- coding: utf-8 -*-
import json
import requests
from sys import exit

from helpers.configfilehelper import get_config_key, YOUTRACK_SECTION, YOUTRACK_KEY, USER_KEY, \
    reset_youtrack_credentials, GLOBAL_SECTION, YT_URL
from services.issueclasses import Issue
from helpers.colors import print_msg, IconsEnum

STATES = {
    "pending": "#{Por hacer}",
    "progress": "#{En progreso}",
    "cr": "#{Para CodeReview}",
    "changes": "#{CR Cambios Solicitados}",
    "qa": "#{Pendiente de QA}",
    "review": "#{En Review}",
    "accepted": "#{Aceptado}",
    "rejected": "#{Rechazado}",
    "all": "#Unresolved"
}


def get_issues_by_state(state):
    if state not in list(STATES.keys()):
        return False

    params = {"fields": "project(shortName),numberInProject,summary,"
                        "fields(projectCustomField(field(name)),value(name))",
              "query": get_youtrack_user() + " " + STATES[state]}

    request_url = get_youtrack_url() + "/api/issues"
    user_request = requests.get(request_url, headers=get_header(), params=params)
    user_list = json.loads(user_request.text)
    if user_request.ok:
        issues = [Issue(issue) for issue in user_list if Issue(issue).state not in ["Archivado", "Backlog"]]
        return issues
    else:
        print_msg(IconsEnum.ERROR, "Error: " + str(user_request.status_code) + " on get_issues_by_state")
        exit()


def get_issue_by_id(id):
    params = {"fields": "description,created,numberInProject,project(shortName),summary,reporter(name),"
                        "fields(projectCustomField(field(name)),value(name))"}
    if id.isdigit():
        request_url = get_youtrack_url() + "/api/issues/RKM-" + id
    else:
        request_url = get_youtrack_url() + "/api/issues/" + id
    user_request = requests.get(request_url, headers=get_header(), params=params)
    if user_request.ok:
        fields = json.loads(user_request.text)
        return Issue(fields, complete=True)
    else:
        print_msg(IconsEnum.ERROR, "Error: " + str(user_request.status_code))
        exit()


def execute_command(issue, field, value):
    request_url = get_youtrack_url() + "/rest/issue/" + issue.id + "/execute?command=" + field + "+" + value
    user_request = requests.post(request_url, headers=get_header())

    if user_request.ok:
        return user_request
    else:
        print_msg(IconsEnum.ERROR, "Error: " + str(user_request.status_code) + " on execute_command")
        exit()


def get_youtrack_user():
    y_user = get_config_key(YOUTRACK_SECTION, USER_KEY)
    if y_user:
        return y_user
    else:
        print_msg(IconsEnum.ERROR, "No has ingresado tus credenciales de Youtrack")
        reset_youtrack_credentials()
        return get_config_key(YOUTRACK_SECTION, USER_KEY)


def get_header():
    y_key = get_config_key(YOUTRACK_SECTION, YOUTRACK_KEY)
    if y_key:
        return {"Authorization": "Bearer "+y_key}
    else:
        print_msg(IconsEnum.ERROR, "No has ingresado tus credenciales de Youtrack")
        reset_youtrack_credentials()
        return get_config_key(YOUTRACK_SECTION, YOUTRACK_KEY)


def get_youtrack_url():
    yt_baseurl = get_config_key(GLOBAL_SECTION, YT_URL)
    return yt_baseurl if yt_baseurl else "https://youtrack.rankmi.com"
