from services.youtrackservice import get_issue_by_id, change_issue_state
from services.githubservice import create_branch
from services.issueclasses import Issue

HEADER = '\033[96m'
GREEN = '\033[92m'
SHOWSTOPPER = '\033[91m',
CRITICAL = '\033[93m'
ENDC = '\033[0m'
BOLD = '\033[1m'

def print_issue(issue):

    print("--------------------------------------------------------------------------")
    print("[" + issue.id + "]",
          "Creado por:", issue.context.reporter,
          "el", issue.context.created)
    print(HEADER + BOLD + issue.summary + ENDC)
    print("[" + issue.state + "]", "[" + issue.priority + "]")
    print("Puedes revisarlo aqui: https://rankmi.myjetbrains.com/youtrack/issue/" + issue.id)
    print("--------------------------------------------------------------------------")

    print(GREEN + BOLD + "Descripcion:" + ENDC)
    print(issue.context.description)
    print("--------------------------------------------------------------------------")

    print(GREEN + BOLD + "Asignados:" + ENDC)
    for field in issue.assignees.listedAssignees:
        print("- "+ BOLD + field + ENDC +":", issue.assignees.listedAssignees[field])
    print("--------------------------------------------------------------------------")

    if issue.state.lower() == "por hacer":
        start_issue(issue)


def print_issue_list(issues, status):
    todo = ["Por hacer", "Por Hacer"]
    prog = ["En progreso", "En curso", "Para CodeReview", "CR Cambios solicitados", "Pendiente de QA", "En review", "Rechazado"]
    open = todo + prog

    issue_ids = []
    index = 0

    for issue in issues:
        if issue.state in eval(status):
            issue_ids.append(issue.id)
            space = "\t" if issue.priority in ["Minor", "Major"] else ""
            color = SHOWSTOPPER + BOLD if issue.priority == "Show-stopper" else ""
            color = CRITICAL + BOLD if issue.priority == "Critical" else ""
            print(color + "[" + str(index) + "] \t", issue.priority, "\t"+space, issue.summary + ENDC)
            index += 1

    try:
        print("--------------------------------------------------------------------------")
        print_issue(get_issue_by_id(issue_ids[int(input(BOLD + "Ingresa el índice del ticket que deseas revisar: " + ENDC))]))
    except (ValueError, IndexError):
        print("Debes ingresar un índice válido.")


def start_issue(issue):
    initializeIssue = input(CRITICAL + BOLD + "Deseas comenzar esta tarea [y/n]: " + ENDC)
    if initializeIssue == "y":
        change_issue_state(issue.id, "En progreso")
        print(HEADER + BOLD + "Estado de la tarea fue cambiado a 'En progreso'" + ENDC)
        createBranch = input(CRITICAL + BOLD + "Deseas crear una rama para esta tarea [y/n]: " + ENDC)
        if createBranch == "y":
            create_branch('master' if issue.priority == "Show-stopper" else 'development', issue.branch)
