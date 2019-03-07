import os
import subprocess

import requests

from alfred.colors import HEADER, BOLD, CRITICAL, GREEN, ENDC
from services.githubservice import create_pr, create_branch
from services.youtrackservice import get_issue_by_id, execute_command, get_header

STATES = {
    "todo": "Por hacer",
    "prog": "En progreso",
    "cr": "Para CodeReview",
    "changes": "CR Cambios Solicitados",
    "qa": "Pendiente de QA",
    "review": "En Review",
    "accepted": "Aceptado",
    "rejected": "Rechazado"
}


def update_issue(action, issue=None):
    actions = {
        "start": start_issue,
        "finish": finish_issue
    }

    action = actions[action]
    action(issue) if issue else action()


def start_issue(issue):
    initializeIssue = input(CRITICAL + BOLD + "Deseas comenzar esta tarea [y/n]: " + ENDC)
    if initializeIssue == "y":
        execute_command(issue.id, "State", STATES["prog"])
        print(HEADER + BOLD + "Estado de la tarea fue cambiado a 'En progreso'" + ENDC)
        createBranch = input(CRITICAL + BOLD + "Deseas crear una rama para esta tarea [y/n]: " + ENDC)
        if createBranch == "y":
            create_branch('master' if issue.priority == "Show-stopper" else 'development', issue.branch)


def finish_issue():
    issue = recognize_current_issue()
    print(HEADER + BOLD + "Finalizando etapa de desarrollo de", issue.id + ENDC)

    prUrl = create_pr('master' if issue.priority == 'Show-stopper' else 'development')
    currentDescription = issue.context.description
    prDescription = currentDescription + "\n\nPR " + os.getcwd().split("/")[-1].upper() + ": " + prUrl
    request_url = "https://rankmi.myjetbrains.com/youtrack/api/issues/" + issue.id + "?fields=description"

    execute_command(issue.id, "State", STATES["cr"])
    print(BOLD + "Tarea actualizada a " + GREEN + "'Para CodeReview'" + ENDC)

    return requests.post(request_url, headers=get_header(), data={'description': prDescription})


def recognize_current_issue():
    currentBranch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])[:-1].decode("utf-8")
    issueId = currentBranch.split("-")[0] + "-" + currentBranch.split("-")[1]
    return get_issue_by_id(issueId)
