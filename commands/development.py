import click

from services.githubservice import upload_asset, create_release
from services.releaser import release_alfred


@click.group(name="dev", help="For Alfred development")
def development():
    pass


@development.command(help="Used for releasing Alfred versions", options_metavar="<option>")
@click.option("--new", is_flag=True, help="Creates a release and uploads a binary for the current OS")
@click.option("-v", "--version", help="Initiates the whole release flow for the given semver", metavar="<semver>")
def release(new, version):
    if new:
        upload_asset(create_release())
    else:
        release_alfred(version)
