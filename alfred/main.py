#!/usr/bin/env python3
"""alfred
"""

import sys

from alfredconfig import AlfredConfig
from configfilehelper import config_file_exists, askcredentials
from awsconfig import AwsConfig
from awsdownloader import getbackup, dumpbackup
import argparse
import click

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
        askcredentials()

@greet.command()
@click.argument('interface')
def reset(interface):
    if interface=="credentials":
        askcredentials()
    else:
        print("Por ahora sólo podemos resetear las credenciales :(")

@greet.command()
@click.argument('environment')
def dump(environment):
    dumpbackup(environment)

if __name__ == '__main__':
    greet(prog_name='alfred.sh')
