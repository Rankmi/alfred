from helpers.issueupdater import update_issue, STATES
from helpers.colors import HEADER, BOLD, ENDC, GREEN, SHOWSTOPPER, CRITICAL, print_msg, IconsEnum
from services.youtrackservice import get_issue_by_id, get_youtrack_url
from services.databaseservice import get_verified_username

SEPARATOR_LENGTH = 75


def print_issue(issue):
    print("-" * SEPARATOR_LENGTH)
    print("[" + issue.id + "]",
          "Creado por:", issue.context.reporter,
          "el", issue.context.created)
    print(HEADER + BOLD + issue.summary + ENDC)
    print("[" + issue.state + "]", "[" + issue.priority + "]")
    print("Puedes revisarlo aqui: " + get_youtrack_url() + "/issue/" + issue.id)
    print("-" * SEPARATOR_LENGTH)

    print(GREEN + BOLD + "Descripcion:" + ENDC)
    print(issue.context.description)
    print("-" * SEPARATOR_LENGTH)

    print(GREEN + BOLD + "Asignados:" + ENDC)
    for field in issue.assignees.listedAssignees:
        print("- " + BOLD + field + ENDC + ":", issue.assignees.listedAssignees[field])
    print("-" * SEPARATOR_LENGTH)

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

        if issue.state in ["Por hacer", "En progreso", "En review", "Rechazado"]:
            state_sep = "\t\t "
        elif issue.state == "CR Cambios solicitados":
            state_sep = " "
        else:
            state_sep = "\t "

        prior_sep = "\t" * (2 if issue.priority == "Minor" else 1)

        print(color + "[" + str(index) + "]\t", issue.priority, prior_sep, issue.state, state_sep, issue.summary + ENDC)
        index += 1

    if len(issue_ids):
        try:
            print("-" * SEPARATOR_LENGTH)
            print_issue(get_issue_by_id(issue_ids[int(input(BOLD + "Ingresa el índice del ticket que deseas revisar: " + ENDC))]))
        except (ValueError, IndexError):
            print("Debes ingresar un índice válido.")
    else:
        print(BOLD + "No tienes tickets para revisar en este estado." + ENDC)


def print_env(env):
    print_msg(IconsEnum.INFO, f"{env.container_name}")
    print("|-- IP:", env.container_ip)
    print("|-- Port:", env.database_port)
    print("|-- DB Username: rankmi-database")
    print("|-- DB Password:", env.database_password)
    print("|-- DB Name:", env.database_name)


def print_envs_list(envs):
    print_msg(IconsEnum.UNICORN, f"Environments creados para {get_verified_username()}")
    for env in envs:
        print("-" * SEPARATOR_LENGTH)
        print_env(env)
    print("-" * SEPARATOR_LENGTH)

