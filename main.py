#!/usr/bin/env python3
"""alfred is your friend, alfred is your god, alfred is nothing
"""

import click

from alfred.awsdownloader import getbackup, dumpbackup
from alfred.configfilehelper import config_file_exists, reset_aws_credentials, reset_youtrack_credentials, \
    reset_github_credentials, reset_everything
from alfred.githubservice import create_repo, create_branch, create_pr
from alfred.youtrackservice import get_my_open_issues, get_issue_by_id
from alfred.printservice import print_issue


@click.group()
def greet():
    pass


@greet.command()
@click.option('--out', '-o', type=click.Path())
@click.option('--extract', is_flag=True)
@click.argument('database_date')
def get(database_date, out, extract):
    if config_file_exists():
        getbackup(database_date, out, extract)
    else:
        reset_aws_credentials()


@greet.command()
@click.argument("interface")
def reset(interface):
    if interface == "aws":
        reset_aws_credentials()
    elif interface == "youtrack":
        reset_youtrack_credentials()
    elif interface == "github":
        reset_github_credentials()
    elif interface == "all":
        reset_everything()
    else:
        print("No conozco esa opción")


@greet.command()
@click.argument("status")
def tasks(status):
    if status == "open":
        get_my_open_issues()


@greet.command()
@click.argument('issue')
def issue(issue):
    print_issue(get_issue_by_id(issue))


@greet.command()
@click.argument("name")
def repo(name):
    create_repo(name)


@greet.command()
@click.argument('repo')
@click.argument('name')
@click.option('--hotfix', '-h', is_flag=True)
def branch(repo, hotfix, name):
    if hotfix:
        create_branch(repo, 'master', name)
    else:
        create_branch(repo, 'development', name)


@greet.command()
@click.argument('repo')
@click.option('--title', '-t', default=None)
@click.option('--rama', '-r')
@click.option('--hotfix', '-h', is_flag=True)
def pr(title, rama, hotfix, repo):
    create_pr(title if title else rama, 'master' if hotfix else 'develop', rama, repo)


@greet.command()
@click.argument('environment')
def dump(environment):
    dumpbackup(environment)


if __name__ == '__main__':
    greet(prog_name='alfred.sh')
