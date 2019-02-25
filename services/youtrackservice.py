# -*- coding: utf-8 -*-
import datetime
import json

import requests

from alfred.configfilehelper import get_config_key, YOUTRACK_SECTION, YOUTRACK_KEY, USER_KEY, \
    reset_youtrack_credentials
from alfred.printer import print_issue

__base_url = "https://rankmi.myjetbrains.com/youtrack/api/"


def get_my_open_issues():
    params = dict(fields="project(shortName),numberInProject,summary",
                  query=get_youtrack_user() + " #unresolved")
    request_url = __base_url + "issues"
    user_request = requests.get(request_url, headers=get_header(), params=params)
    user_list = json.loads(user_request.text)
    issues = []
    for n in range(len(user_list)):
        deserialized_user = User(user_list[n]['summary'], user_list[n]['numberInProject'], user_list[n]['project'])
        issues.append(deserialized_user.project['shortName'] + "-" + str(deserialized_user.numberInProject))
        print("[" + str(n) + "]", deserialized_user)

    try:
        print_issue(get_issue_by_id(issues[int(input("Ingresa el índice del ticket que deseas revisar: "))]))
    except (ValueError, IndexError):
        print("Debes ingresar un índice válido.")

def get_issue_by_id(id):
    params = dict(fields="description,created,numberInProject,project(shortName),summary,reporter(name),"
                         "fields(projectCustomField(field(name)),value(name))")
    if id.isdigit():
        request_url = __base_url + "issues/RKM-" + id
    else:
        request_url = __base_url + "issues/" + id
    user_request = requests.get(request_url, headers=get_header(), params=params)
    fields = json.loads(user_request.text)
 
    usefulFields = {
        "project": fields['project']['shortName'],
        "numberInProject": str(fields['numberInProject']),
        "summary": fields['summary'],
        "reporter": fields['reporter']['name'],
        "created": datetime.datetime.fromtimestamp( fields['created'] / 1000).strftime("%B %d, %Y"),
        "description": fields['description'],
        "assignees": {}
        
    }

    requiredCustoms = ["State", "Priority"]
    requiredAssignees = ["Responsable", "Revisor", "Diseñador(a)", "Code reviewer", "Jefe de proyecto"]

    for field in fields['fields']:

        fieldName = field['projectCustomField']['field']['name']
        fieldValue = field['value']

        if fieldName in requiredCustoms:
            usefulFields[fieldName] = fieldValue['name'] if fieldValue else None
            
        elif fieldName in requiredAssignees:
            usefulFields["assignees"][fieldName] = fieldValue['name'] if fieldValue else None

    return usefulFields


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
