from helpers.issueupdater import update_issue, STATES
from helpers.colors import HEADER, BOLD, ENDC, GREEN, SHOWSTOPPER, CRITICAL
from services.youtrackservice import get_issue_by_id
from helpers.configfilehelper import get_config_key, GLOBAL_SECTION, YT_URL


def print_issue(issue):

    print("--------------------------------------------------------------------------")
    print("[" + issue.id + "]",
          "Creado por:", issue.context.reporter,
          "el", issue.context.created)
    print(HEADER + BOLD + issue.summary + ENDC)
    print("[" + issue.state + "]", "[" + issue.priority + "]")
    print("Puedes revisarlo aqui: " + get_config_key(GLOBAL_SECTION, YT_URL) + "/issue/" + issue.id)
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

    if issues == 400:
        print("Debes ingresar un estado válido. Revisa la documentación en https://github.com/Rankmi/alfred.")
        return 400

    issue_ids = [issue.id for issue in issues]
    index = 0

    for issue in issues:
        if issue.priority == "ShowStopper":
            color = SHOWSTOPPER + BOLD
        elif issue.priority == "Blocker":
            color = CRITICAL + BOLD
        else:
            color = ""
        print(color + "[" + str(index) + "] \t", issue.priority, "\t", issue.summary + ENDC)
        index += 1

    if len(issue_ids):
        try:
            print("--------------------------------------------------------------------------")
            print_issue(get_issue_by_id(issue_ids[int(input(BOLD + "Ingresa el índice del ticket que deseas revisar: " + ENDC))]))
        except (ValueError, IndexError):
            print("Debes ingresar un índice válido.")
    else:
        print(BOLD + "No tienes tickets para revisar en este estado." + ENDC)
