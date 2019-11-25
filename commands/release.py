import click
import requests

from data.Releaser import ReleaseRankmiResponse, ReleaseProjectResponse
from services.releaser import get_releaser_url, rel_rankmi_response, rel_project_response
from services.youtrackservice import get_youtrack_user


@click.group(name='release', help='Automatization of the release flow')
def release():
    pass


@release.command(name='rankmi', help="Used to release Rankmi versions")
@click.option("--app", default=None)
@click.option("--api", default=None)
def rankmi(app_v, api_v):
    request_url = get_releaser_url() + "/release"
    response = requests.post(url=request_url,
                             json={
                                 "author": get_youtrack_user(),
                                 "app_version": app_v,
                                 "api_version": api_v})
    rel_rankmi_response(ReleaseRankmiResponse.from_dict(response.json()))


@release.command(name='project', help='Used to release other projects in Rankmi')
@click.option("-n", "--name", required=True)
@click.option("-v", "--version", default=None)
def project(name, version):
    request_url = get_releaser_url() + "/release-project"
    response = requests.post(url=request_url,
                             json={
                                 "author": get_youtrack_user(),
                                 "project": {
                                     "name": name,
                                     "version": version
                                 }
                             })
    rel_project_response(ReleaseProjectResponse.from_dict(response.json()))
