import os
import subprocess

import requests

from alfred.colors import HEADER, BOLD, CRITICAL, GREEN, ENDC
from services.githubservice import create_pr, create_branch, delete_branch
from services.youtrackservice import get_issue_by_id, execute_command, get_header

STATES = {
    "todo": "Por hacer",
    "prog": "En progreso",
    "cr": "Para CodeReview",
    "changes": "CR Cambios Solicitados",
    "qa": "Pendiente de QA",
    "review": "En Review",
    "accepted": "Aceptado",
    "reject": "Rechazado",
    "production": "Producción"
}


def update_issue(action, issue=None):
    actions = {
        "start": start_issue,
        "finish": finish_issue,
        "accept": accept_issue,
        "changes": move_issue,
        "qa": move_issue,
        "review": move_issue,
        "reject": move_issue
    }

    update = actions[action]
    if action in ["changes", "qa", "review", "reject"]:
        update(action)
    else:
        update(issue) if issue else update()


def start_issue(issue):
    initialize_issue = input(CRITICAL + BOLD + "Deseas comenzar esta tarea [y/n]: " + ENDC)
    if initialize_issue == "y":
        execute_command(issue, "State", STATES["prog"])
        print(BOLD + "Estado de la tarea fue cambiado a 'En progreso'" + ENDC)
        generate_branch = input(CRITICAL + BOLD + "Deseas crear una rama para esta tarea [y/n]: " + ENDC)
        if generate_branch == "y":
            create_branch('master' if issue.priority == "Show-stopper" else 'development', issue.branch)


def finish_issue():
    issue = recognize_current_issue()
    print(HEADER + BOLD + "Finalizando etapa de desarrollo de", issue.id + ENDC)

    pr_url = create_pr('master' if issue.priority == 'Show-stopper' else 'development')
    execute_command(issue, "State", STATES["cr"])
    print(BOLD + "Estado de la tarea fue cambiado a " + GREEN + "'Para CodeReview'" + ENDC)

    current_description = issue.context.description if issue.context.description else ""
    pr_description = current_description + "\n\nPR " + os.getcwd().split("/")[-1].title() + ":\n" + pr_url
    request_url = "https://rankmi.myjetbrains.com/youtrack/api/issues/" + issue.id + "?fields=description"
    user_request = requests.post(request_url, headers=get_header(), json={'description': pr_description})
    print(HEADER + BOLD + "Pullrequest agregado a descripción del ticket" + ENDC)

    print(BOLD + "Volviendo a " + GREEN + "'development'" + ENDC)
    subprocess.run(["git", "checkout", "development"])
    subprocess.run(["git", "pull", "origin", "development"])
    return user_request


def accept_issue():
    issue = recognize_current_issue()
    print(HEADER + BOLD + "Finalizando etapa de QA de", issue.id + ENDC)

    if issue.priority == 'Show-stopper':
        execute_command(issue, "State", STATES["production"])
        print(BOLD + "Estado de la tarea fue cambiado a " + GREEN + "'Producción'" + ENDC)
    else:
        execute_command(issue, "State", STATES["accepted"])
        print(BOLD + "Estado de la tarea fue cambiado a " + GREEN + "'Aceptado'" + ENDC)
    delete_branch(issue.branch)
    print(HEADER + BOLD + "La rama de " + os.getcwd().split("/")[-1].title() + " fue eliminada" + ENDC)


def move_issue(action):
    issue = recognize_current_issue()
    execute_command(issue, "State", STATES[action])
    print(BOLD + "Estado de la tarea fue cambiado a '" + GREEN + STATES[action] + "'" + ENDC)
    if action != 'review':
        subprocess.run(["git", "checkout", "development"])
        subprocess.run(["git", "pull", "origin", "development"])


def recognize_current_issue():
    current_branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])[:-1].decode("utf-8")
    issue_id = current_branch.split("-")[0] + "-" + current_branch.split("-")[1]
    return get_issue_by_id(issue_id)
