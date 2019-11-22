import click

from helpers.configfilehelper import reset_aws_credentials, reset_github_credentials, reset_kato_credentials, \
    reset_youtrack_credentials, reset_all_credentials, reset_releaser_credentials


@click.group(help="Helps configuring credentials")
def reset():
    pass


@reset.command(help="Resets AWS' credentials")
def aws():
    reset_aws_credentials()


@reset.command(help="Resets Github's credentials")
def github():
    reset_github_credentials()


@reset.command(help="Resets Kato's credentials")
def kato():
    reset_kato_credentials()


@reset.command(help="Resets Youtrack's credentials")
def youtrack():
    reset_youtrack_credentials()


@reset.command(help="Resets Releaser's credentials")
def releaser():
    reset_releaser_credentials()


@reset.command(name='all', help='Resets credentials for every service used by Alfred')
def reset_all():
    reset_all_credentials()
