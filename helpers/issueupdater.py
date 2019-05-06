import os
import subprocess

import requests
from halo import Halo

from helpers.colors import HEADER, BOLD, CRITICAL, GREEN, ENDC
from services.githubservice import create_pr, create_branch, delete_branch
from services.youtrackservice import get_issue_by_id, execute_command, get_header
from helpers.configfilehelper import GLOBAL_SECTION, YT_URL, get_config_key

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
    spinner = Halo()

    initialize_issue = input(CRITICAL + BOLD + "Deseas comenzar esta tarea [y/n]: " + ENDC)
    if initialize_issue == "y":
        execute_command(issue, "State", STATES["prog"])
        spinner.succeed(BOLD + "Estado de la tarea fue cambiado a 'En progreso'" + ENDC)
        generate_branch = input(CRITICAL + BOLD + "Deseas crear una rama para esta tarea [y/n]: " + ENDC)
        if generate_branch == "y":
            create_branch('master' if issue.priority in ["ShowStopper", "Blocker"] else 'development', issue.branch)


def finish_issue():
    issue = recognize_current_issue()

    spinner = Halo(text=HEADER + BOLD + "Finalizando etapa de desarrollo de " + issue.id + ENDC, spinner="dots")
    spinner.stop_and_persist(symbol='🦄'.encode('utf-8'))

    pr_url = create_pr('master' if issue.priority in ["ShowStopper", "Blocker"] else 'development')
    execute_command(issue, "State", STATES["cr"])
    spinner.succeed(BOLD + "Estado de la tarea fue cambiado a " + GREEN + "'Para CodeReview'" + ENDC)

    spinner.start("Agregando Pull-Request al ticket")
    current_description = issue.context.description if issue.context.description else ""
    pr_description = current_description + "\n\nPR " + os.getcwd().split("/")[-1].title() + ":\n" + pr_url + " *via **alfred***"
    request_url = get_config_key(GLOBAL_SECTION, YT_URL) + "/api/issues/" + issue.id + "?fields=description"
    user_request = requests.post(request_url, headers=get_header(), json={'description': pr_description})
    spinner.succeed(HEADER + BOLD + "Pull-Request agregado a descripción del ticket" + ENDC)

    spinner.start(BOLD + "Volviendo a " + GREEN + "'development'" + ENDC)
    subprocess.run(["git", "checkout", "development"])
    subprocess.run(["git", "pull", "origin", "development"])
    spinner.succeed()
    return user_request


def accept_issue():
    issue = recognize_current_issue()

    spinner = Halo(text=HEADER + BOLD + "Finalizando etapa de QA de " + issue.id + ENDC, spinner="dots")
    spinner.stop_and_persist(symbol='🦄'.encode('utf-8'))

    if issue.priority in ["ShowStopper", "Blocker"]:
        execute_command(issue, "State", STATES["production"])
        spinner.succeed(BOLD + "Estado de la tarea fue cambiado a " + GREEN + "'Producción'" + ENDC)
    else:
        execute_command(issue, "State", STATES["accepted"])
        spinner.succeed(BOLD + "Estado de la tarea fue cambiado a " + GREEN + "'Aceptado'" + ENDC)
    delete_branch(issue.branch)
    print(HEADER + BOLD + "La rama de " + os.getcwd().split("/")[-1].title() + " fue eliminada" + ENDC)


def move_issue(action):
    issue = recognize_current_issue()
    spinner = Halo()

    execute_command(issue, "State", STATES[action])
    spinner.stop_and_persist(text=BOLD + "Estado de la tarea fue cambiado a '" + GREEN + STATES[action] + "'" + ENDC,
                             symbol='🦄'.encode('utf-8'))

    if action != 'review':
        subprocess.run(["git", "checkout", "development"])
        subprocess.run(["git", "pull", "origin", "development"])


def recognize_current_issue():
    current_branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])[:-1].decode("utf-8")
    issue_id = current_branch.split("-")[0] + "-" + current_branch.split("-")[1]
    return get_issue_by_id(issue_id)
