import click

from helpers.colors import print_msg, IconsEnum
from helpers.issueupdater import update_issue
from helpers.printer import print_issue_list, print_issue
from services.githubservice import is_folder_github_repo
from services.youtrackservice import get_issues_by_state, get_issue_by_id


@click.group(help="Utils for Youtrack Issues")
def issues():
    pass


@issues.command(name="update", help="Updates the current issue to a certain state")
@click.argument("action")
def update_current_issue(action):
    if is_folder_github_repo():
        update_issue(action)
    else:
        print_msg(IconsEnum.ERROR, 'Debes localizarte en un repositorio válido')
        exit()


@issues.command(name="state", help="Prints the list of issues in a given state")
@click.argument("state")
def print_tasks_by_state(state):
    print_issue_list(get_issues_by_state(state))


@issues.command(name="get", help="Prints the issue associated to the given ID")
@click.argument("issue")
def print_issue_by_id(issue):
    print_issue(get_issue_by_id(issue))
