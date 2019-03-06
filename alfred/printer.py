from alfred.issueupdater import update_issue, STATES
from alfred.colors import HEADER, BOLD, ENDC, GREEN, SHOWSTOPPER, CRITICAL
from services.youtrackservice import get_issue_by_id


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

    if issue.state == STATES["todo"]:
        update_issue("start", issue)


def print_issue_list(issues):
    issue_ids = [issue.id for issue in issues]
    index = 0

    for issue in issues:
        space = "\t" if issue.priority in ["Minor", "Major"] else ""
        color = SHOWSTOPPER + BOLD if issue.priority == "Show-stopper" else ""
        color = CRITICAL + BOLD if issue.priority == "Critical" else ""
        print(color + "[" + str(index) + "] \t", issue.priority, "\t"+space, issue.summary + ENDC)
        index += 1

    if len(issue_ids):
        try:
            print("--------------------------------------------------------------------------")
            print_issue(get_issue_by_id(issue_ids[int(input(BOLD + "Ingresa el índice del ticket que deseas revisar: " + ENDC))]))
        except (ValueError, IndexError):
            print("Debes ingresar un índice válido.")
    else:
        print(BOLD + "No tienes tickets para revisar en este estado." + ENDC)
