#!/usr/bin/env python3
"""alfred is your friend, alfred is your god, alfred is nothing
"""

import click

from awsdownloader import getbackup, dumpbackup
from configfilehelper import config_file_exists, reset_aws_credentials, reset_youtrack_credentials, \
    reset_github_credentials, reset_everything
from githubservice import create_repo, create_branch, create_pr
from youtrackservice import get_my_open_issues


@click.group()
def greet():
    pass


@greet.command()
@click.argument('database_date')
@click.option('--out', '-o', type=click.Path())
def get(database_date, out):
    if config_file_exists():
        getbackup(database_date, out)
    else:
        reset_aws_credentials()


@greet.command()
@click.argument("interface")
def reset(interface):
    if interface == "credentials":
        reset_aws_credentials()
    elif interface == "youtrack-credentials":
        reset_youtrack_credentials()
    elif interface == "github-credentials":
        reset_github_credentials()
    elif interface == "everything":
        reset_everything()
    else:
        print("No conozco esa opción")


@greet.command()
@click.argument("status")
def tasks(status):
    if status == "open":
        get_my_open_issues()


@greet.command()
@click.argument("name")
def repos(name):
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
@click.option('--title', '-t')
@click.option('--base', '-b')
@click.option('--rama', '-r')
def pr(title, base, rama, repo):
    create_pr(title, base, rama, repo)

@greet.command()
@click.argument('environment')
def dump(environment):
    dumpbackup(environment)


if __name__ == '__main__':
    greet(prog_name='alfred.sh')
