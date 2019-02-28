# -*- coding: utf-8 -*-
import json

import requests

from alfred.configfilehelper import get_config_key, YOUTRACK_SECTION, YOUTRACK_KEY, USER_KEY, \
    reset_youtrack_credentials
from services.issueclasses import Issue, Context, Assignees

__base_url = "https://rankmi.myjetbrains.com/youtrack/api/"


def get_my_open_issues():
    params = dict(fields="project(shortName),numberInProject,summary,"
                         "fields(projectCustomField(field(name)),value(name))",
                  query=get_youtrack_user() + " #unresolved")
    request_url = __base_url + "issues"
    user_request = requests.get(request_url, headers=get_header(), params=params)
    user_list = json.loads(user_request.text)
    
    issues = []

    for issue in user_list:
        issues.append(Issue(issue))
    
    return issues


def get_issue_by_id(id):
    params = dict(fields="description,created,numberInProject,project(shortName),summary,reporter(name),"
                         "fields(projectCustomField(field(name)),value(name))")
    if id.isdigit():
        request_url = __base_url + "issues/RKM-" + id
    else:
        request_url = __base_url + "issues/" + id
    user_request = requests.get(request_url, headers=get_header(), params=params)
    fields = json.loads(user_request.text)

    return Issue(fields, complete=True)


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
