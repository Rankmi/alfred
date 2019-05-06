import datetime
from sys import exit

import boto3
import botocore
from tqdm import tqdm
from halo import Halo

from helpers.configfilehelper import get_config_key, AWS_SECTION, USER_KEY, reset_aws_credentials, PASS_KEY, \
    AWS_BUCKET_KEY
from helpers.filehelper import uncompress


def hook(t):
    def inner(bytes_amount):
        t.update(bytes_amount)

    return inner


def get_backup(key, destination_file=None, uncompress_file=False, delete_after_extraction=False):
    if key == 'todaydb':
        filename = datetime.datetime.now().strftime('%Y_%m_%d')
    else:
        filename = key

    if destination_file is None:
        destination_file = 'backup_reducido_' + filename + '.tar.xz'

    awsfile = 'backup_reducido_' + filename + '.tar.xz'

    download_file(destination_file, awsfile)

    if uncompress_file:
        uncompress(filepath=destination_file, delete_after=delete_after_extraction)


def download_file(destination_file, aws_file):
    aws_access_key = get_aws_access_key()
    aws_secret = get_aws_access_secret()
    aws_bucket = get_aws_bucket()
    spinner = Halo()

    resource = boto3.resource('s3', region_name='us-west-2',
                              aws_access_key_id=aws_access_key,
                              aws_secret_access_key=aws_secret)

    fileobject = resource.Object(aws_bucket, aws_file)
    try:
        spinner.start('Comenzando la descarga')
        filesize = fileobject.content_length
        spinner.stop_and_persist(symbol='🦄'.encode('utf-8'))
        with tqdm(total=filesize, unit='B', unit_scale=True,
                  desc=destination_file) as t:
            resource.Bucket(aws_bucket).download_file(aws_file, destination_file, Callback=hook(t))
        spinner.succeed('Descarga finalizada')
        return True
    except botocore.exceptions.ParamValidationError as e:
        spinner.fail("El bucket no tiene el nombre correcto. Resetea tus credenciales" +
                     "(alfred reset aws)")
        exit()
    except botocore.exceptions.ClientError as e:
        spinner.fail("Error " + e.response['Error']['Code'])
        exit()
    except ValueError:
        spinner.fail("No se pudo descargar el archivo por problemas de conectividad")
        exit()


def dumpbackup(key):
    aws_access_key = get_aws_access_key()
    aws_secret = get_aws_access_secret()

    if (key == 'production') or (key == 'staging') or (key == 'development'):
        # revisar si la maquina esta encendida, si lo esta solicitar intentar nuevamente, sino lo esta entonces encender
        print('Batman, the dump of the ' + key + ' environment is starting...')
        instances = ['i-0b08005bfb8829080']
        resource = boto3.client('ec2', region_name='us-west-2',
                                aws_access_key_id=aws_access_key,
                                aws_secret_access_key=aws_secret)
        status = resource.describe_instance_status(InstanceIds=instances)
        if not status.get("InstanceStatuses"):
            print("Starting dump... Batman should wait aprox 30min to complete this asynchronous task...")
            print("To download this dump please use this command:")
            print("")
            print("--->>>> main.py get " + key + "_DD_MM_YY")
            print("")
            s3 = boto3.resource('s3', region_name='us-west-2',
                                aws_access_key_id=aws_access_key,
                                aws_secret_access_key=aws_secret)
            object = s3.Object('rankmi-backup-semanal', 'backup-type.dat')
            object.put(Body=key)
            resource.start_instances(InstanceIds=instances)
        else:
            print("Hay otro Dump en proceso, por favor intentende nuevo en unos minutos...")
    else:
        print('Batman, debes indicar el ambiente correctamente...')


def get_aws_access_key():
    aws_access_key = get_config_key(AWS_SECTION, USER_KEY)
    if aws_access_key:
        return aws_access_key
    else:
        reset_aws_credentials()
        return get_config_key(AWS_SECTION, USER_KEY)


def get_aws_access_secret():
    aws_access_secret = get_config_key(AWS_SECTION, PASS_KEY)
    if aws_access_secret:
        return aws_access_secret
    else:
        reset_aws_credentials()
        return get_config_key(AWS_SECTION, PASS_KEY)


def get_aws_bucket():
    aws_bucket = get_config_key(AWS_SECTION, AWS_BUCKET_KEY)
    if aws_bucket:
        return aws_bucket
    else:
        reset_aws_credentials()
        return get_config_key(AWS_SECTION, AWS_BUCKET_KEY)
