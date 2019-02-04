from pathlib import Path
import os
import configparser
from awsconfig import AwsConfig
from configparser import ConfigParser


__configfilename = '.alfred.conf'
configlocation = Path(os.path.join(Path.home(), __configfilename))

def askcredentials():
    key = input('User: ')
    secret = getpass.getpass('Password: ')
    bucket = input('Bucket (default = rankmi-backup-semanal) : ')
    if not bucket:
        bucket = 'rankmi-backup-semanal'
    set_config_file(AlfredConfig(key, secret, bucket))

def config_file_exists():
    if configlocation.is_file():
        return True
    else:
        return False

def set_config_file(userconfig):
    config = configparser.ConfigParser()
    config.optionxform = str
    config['AWS'] = {}
    config['AWS']['User'] = userconfig.user
    config['AWS']['Pass'] = userconfig.password
    config['DIARIOS'] = {}
    config['DIARIOS']['Bucket'] = userconfig.bucket
    with open(configlocation, "w+") as file:
        config.write(file)
        print("Archivo de configuración actualizado")

def readconfig() -> AwsConfig:
    parser = ConfigParser()
    parser.read(configlocation)
    return AwsConfig(parser.get('AWS', 'User'),
                     parser.get('AWS', 'Pass'),
                     parser.get('DIARIOS', 'Bucket'))
