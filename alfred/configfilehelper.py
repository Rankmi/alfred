# -*- coding: utf-8 -*-
import configparser
import getpass
from configparser import ConfigParser
from os.path import join
from pathlib import Path

from .alfredconfig import AlfredConfig
from .awsconfig import AwsConfig

__config_filename = '.alfred.conf'
config_location = Path(join(str(Path.home()), __config_filename))

AWS_SECTION = "AWS"
GITHUB_SECTION = "GITHUB"
YOUTRACK_SECTION = "YOUTRACK"

USER_KEY = "User"
PASS_KEY = "Pass"
YOUTRACK_KEY = "Key"


def reset_aws_credentials():
    key = input("User: ")
    secret = getpass.getpass("Password: ")
    bucket = input("Bucket (default = rankmi-backup-semanal) : ")
    if not bucket:
        bucket = "rankmi-backup-semanal"
    set_config_file(AlfredConfig(key, secret, bucket))


def reset_youtrack_credentials():
    youtrack_key = input("Youtrack Key: ")
    youtrack_username = input("Youtrack Username: ")
    set_config_file(AlfredConfig(youtrack_token=youtrack_key, youtrack_username=youtrack_username))


def reset_github_credentials():
    github_username = input("Github Username: ")
    github_password = getpass.getpass("Github Password: ")
    set_config_file(AlfredConfig(github_username=github_username, github_password=github_password))


def reset_everything():
    reset_aws_credentials()
    reset_youtrack_credentials()
    reset_github_credentials()


def config_file_exists():
    if config_location.is_file():
        return True
    else:
        return False


def set_config_file(user_config):
    config = configparser.ConfigParser()
    config.optionxform = str
    config[AWS_SECTION] = {}
    if user_config.user is not None:
        config[AWS_SECTION][USER_KEY] = user_config.user
    if user_config.password is not None:
        config[AWS_SECTION][PASS_KEY] = user_config.password
    config['DIARIOS'] = {}
    if user_config.bucket is not None:
        config['DIARIOS']['Bucket'] = user_config.bucket
    config[YOUTRACK_SECTION] = {}
    if user_config.youtrack_token is not None:
        config[YOUTRACK_SECTION][YOUTRACK_KEY] = user_config.youtrack_token
    if user_config.youtrack_username is not None:
        config[YOUTRACK_SECTION][USER_KEY] = user_config.youtrack_username
    config[GITHUB_SECTION] = {}
    if user_config.github_username is not None:
        config[GITHUB_SECTION][USER_KEY] = user_config.github_username
    if user_config.github_password is not None:
        config[GITHUB_SECTION][PASS_KEY] = user_config.github_password

    with open(str(config_location), "w+") as file:
        config.write(file)


def readconfig() -> AwsConfig:
    parser = ConfigParser()
    parser.read(config_location)
    return AwsConfig(parser.get(AWS_SECTION, USER_KEY),
                     parser.get(AWS_SECTION, PASS_KEY),
                     parser.get('DIARIOS', 'Bucket'))


def get_config_key(section, key):
    parser = ConfigParser()
    parser.read(config_location)
    if parser.has_section(section) and parser.has_option(section, key):
        return parser.get(section, key)
    else:
        return None


def read_youtrack_username() -> str:
    parser = ConfigParser()
    parser.read(config_location)
    return parser.get(AWS_SECTION, USER_KEY)
