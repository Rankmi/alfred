import os
import subprocess
from sys import exit

import requests

from helpers.colors import HEADER, BOLD, CRITICAL, GREEN, ENDC, print_msg, IconsEnum
from services.githubservice import create_pr, hubflow_interaction, is_folder_github_repo
from services.issueclasses import YoutrackPriorities
from services.youtrackservice import get_issue_by_id, execute_command, get_header, get_youtrack_url

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
        print_msg(IconsEnum.SUCCESS, "Estado de la tarea fue cambiado a 'En progreso'")
        if not is_folder_github_repo(): exit()

        generate_branch = input(CRITICAL + BOLD + "Deseas crear una rama para esta tarea [y/n]: " + ENDC)
        if generate_branch == "y":
            priority = 'hotfix' if issue.priority in YoutrackPriorities.HOTFIXES.value else 'feature'
            hubflow_interaction('start', priority, issue.id)


def finish_issue(issueid):
    issue = get_issue_by_id(issueid)

    print_msg(IconsEnum.UNICORN, "Finalizando etapa de desarrollo de " + HEADER + issue.id)
    pr_url = create_pr('development', issue)
    execute_command(issue, "State", STATES["cr"])
    print_msg(IconsEnum.SUCCESS, "Estado de la tarea fue cambiado a " + GREEN + "'Para CodeReview'")

    print_msg(IconsEnum.INFO, "Agregando Pull-Request al ticket")
    current_description = issue.context.description if issue.context.description else ""
    pr_description = current_description + "\n\nPR " + \
                     os.getcwd().split("/")[-1].title() + ":\n" + pr_url + " *via **alfred***"
    request_url = get_youtrack_url() + "/api/issues/" + issue.id + "?fields=description"
    user_request = requests.post(request_url, headers=get_header(), json={'description': pr_description})
    print_msg(IconsEnum.SUCCESS, "Pull-Request agregado a descripción del ticket")

    print_msg(IconsEnum.INFO, "Volviendo a " + GREEN + "'development'")
    subprocess.run(["git", "checkout", "development"])
    subprocess.run(["git", "hf", "update"])
    
    return user_request


def accept_issue():
    issue = recognize_current_issue()
    current_branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])[:-1].decode("utf-8")

    print_msg(IconsEnum.UNICORN, "Finalizando etapa de QA de " + HEADER + issue.id)

    if issue.priority in ["ShowStopper", "Blocker", "Critical"]:
        subprocess.run(['git', 'hf', 'hotfix', 'finish', current_branch.split('/')[1]])
        execute_command(issue, "State", STATES["production"])
        print_msg(IconsEnum.SUCCESS, "Estado de la tarea fue cambiado a " + GREEN + "'Producción'")
    else:
        subprocess.run(['git', 'hf', 'feature', 'finish', current_branch.split('/')[1]])
        execute_command(issue, "State", STATES["accepted"])
        print_msg(IconsEnum.SUCCESS, "Estado de la tarea fue cambiado a " + GREEN + "'Aceptado'")


def move_issue(action):
    issue = recognize_current_issue()

    execute_command(issue, "State", STATES[action])
    print_msg(IconsEnum.UNICORN, "Estado de la tarea fue cambiado a '" + GREEN + STATES[action] + "'"),

    if action != 'review':
        subprocess.run(["git", "checkout", "development"])
        subprocess.run(["git", "pull", "origin", "development"])


def recognize_current_issue():
    current_branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])[:-1].decode("utf-8")
    issue_id = "-".join(current_branch.split("-")[:2]).split("/")[1]
    return get_issue_by_id(issue_id)
