import click
import requests

from services.releaser import get_releaser_url


@click.command(name="release", help="Used to release Rankmi versions")
@click.option("--app-v", default=None)
@click.option("--api-v", default=None)
def release(app_v, api_v):
    request_url = get_releaser_url() + "/release"
    response = requests.post(request_url,
                             json={
                                 "author": "",
                                 "app_version": app_v,
                                 "api_version": api_v},
                             headers={
                                 "Content-type": "application/json"})
    return response.json()
