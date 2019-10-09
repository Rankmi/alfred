import click

from services.awsservice import get_backup, dumpbackup


@click.group(name="db", help="Used for managing the AWS Database service")
def database():
    pass


@database.command(name='get', help='Downloads a S3 Database for a given date ("today" is valid)')
@click.option('--out', '-o', type=click.Path())
@click.option('--extract', is_flag=True)
@click.option('--delete', is_flag=True)
@click.argument('database_date')
def download_database(database_date, out, extract, delete):
    get_backup(database_date, out, extract, delete)


@database.command(help="Tells AWS to create a backup of a database for a given environment")
@click.argument("environment")
def dump(environment):
    dumpbackup(environment)
