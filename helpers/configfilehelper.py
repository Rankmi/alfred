# -*- coding: utf-8 -*-
import configparser
import getpass
from configparser import ConfigParser
from os.path import expanduser

from config_models.alfredconfig import AlfredConfig

__config_filename = '.alfred.conf'
config_location = str(expanduser("~") + "/" + __config_filename)

AWS_SECTION = "AWS"
GITHUB_SECTION = "GITHUB"
YOUTRACK_SECTION = "YOUTRACK"
GLOBAL_SECTION = "GLOBAL"

USER_KEY = "User"
PASS_KEY = "Pass"
YOUTRACK_KEY = "Key"
AWS_BUCKET_KEY = "Bucket"
GH_TOKEN = "Token"
YT_URL = "BaseUrl"


def reset_credentials(interface):
    interfaces = {
        "aws": reset_aws_credentials,
        "youtrack": reset_youtrack_credentials,
        "github": reset_github_credentials,
        "global": reset_global_credentials,
        "all": reset_all_credentials
    }

    if interface not in list(interfaces.keys()):
        print("Debes ingresar un input válido. Revisa la documentación en https://github.com/Rankmi/alfred.")
        return 400

    reset = interfaces[interface]
    reset()


def reset_aws_credentials():
    key = input("AWS User: ")
    secret = getpass.getpass("AWS Password: ")
    bucket = input("AWS Bucket (default = rankmi-backup-semanal) : ")
    if not bucket:
        bucket = "rankmi-backup-semanal"
    set_config_file(AlfredConfig(user=key, password=secret, bucket=bucket))


def reset_youtrack_credentials():
    youtrack_key = input("Youtrack Key: ")
    youtrack_username = input("Youtrack Username: ")
    set_config_file(AlfredConfig(youtrack_token=youtrack_key, youtrack_username=youtrack_username))


def reset_github_credentials():
    github_username = input("Github Username: ")
    github_password = getpass.getpass("Github Password: ")
    set_config_file(AlfredConfig(github_username=github_username, github_password=github_password))


def reset_global_credentials():
    youtrack_url = input("Youtrack URL: ")
    github_token = input("Github Token: ")
    if not youtrack_url:
        youtrack_url = "https://youtrack.rankmi.com"
    set_config_file(AlfredConfig(github_token=github_token, youtrack_url=youtrack_url))


def reset_all_credentials():
    reset_aws_credentials()
    reset_youtrack_credentials()
    reset_github_credentials()


def config_file_exists():
    return config_location.is_file()


def set_config_file(user_config):
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(config_location)
    if user_config.user and user_config.password:
        config[AWS_SECTION] = {}
        config[AWS_SECTION][USER_KEY] = user_config.user
        config[AWS_SECTION][PASS_KEY] = user_config.password
        config[AWS_SECTION][AWS_BUCKET_KEY] = user_config.bucket
    if user_config.youtrack_token and user_config.youtrack_username:
        config[YOUTRACK_SECTION] = {}
        config[YOUTRACK_SECTION][YOUTRACK_KEY] = user_config.youtrack_token
        config[YOUTRACK_SECTION][USER_KEY] = user_config.youtrack_username
    if user_config.github_username and user_config.github_password:
        config[GITHUB_SECTION] = {}
        config[GITHUB_SECTION][USER_KEY] = user_config.github_username
        config[GITHUB_SECTION][PASS_KEY] = user_config.github_password
    if user_config.youtrack_url and user_config.github_token:
        config[GLOBAL_SECTION] = {}
        config[GLOBAL_SECTION][YT_URL] = user_config.youtrack_url
        config[GLOBAL_SECTION][GH_TOKEN] = user_config.github_token

    with open(str(config_location), "w+") as file:
        config.write(file)


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
