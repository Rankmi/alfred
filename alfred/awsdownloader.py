import boto3
import datetime
import botocore
from tqdm import tqdm
from configfilehelper import readconfig


def hook(t):
    def inner(bytes_amount):
        t.update(bytes_amount)

    return inner


def getbackup(key, destination_file=None):
    awsconfig = readconfig()
    resource = boto3.resource('s3', region_name='us-west-2',
                              aws_access_key_id=awsconfig.key,
                              aws_secret_access_key=awsconfig.secret)
    if key == 'todaydb':
        filename = datetime.datetime.now().strftime('%Y_%m_%d')
    else:
        filename = key

    if destination_file is None:
        destination_file = 'backup_reducido_' + filename + '.tar.xz'

    print('Starting Download')

    awsfile = 'backup_reducido_' + filename + '.tar.xz'
    fileobject = resource.Object(awsconfig.bucket, awsfile)
    try:
        filesize = fileobject.content_length
    except botocore.exceptions.ParamValidationError as e:
        print("El bucket no tiene el nombre correcto. Resetea tus credenciales" +
              "(./alfred.sh reset credentials)")
        exit()
    except botocore.exceptions.ClientError as e:
        print("Error " + e.response['Error']['Code'])
        print("Resetea tus credenciales (./alfred.sh reset credentials)")
        exit()
    try:
        with tqdm(total=filesize, unit='B', unit_scale=True,
                  desc=destination_file) as t:
            resource.Bucket(awsconfig.bucket).download_file(awsfile, destination_file, Callback=hook(t))
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("There's no database... Try with the following format YYYY_MM_DD")
        else:
            raise


def dumpbackup(key):
    awsconfig = readconfig()
    if (key == 'production') or (key == 'staging') or (key == 'development'):
        # revisar si la maquina esta encendida, si lo esta solicitar intentar nuevamente, sino lo esta entonces encender
        print('Batman, the dump of the ' + key + ' environment is starting...')
        instances = ['i-0b08005bfb8829080']
        resource = boto3.client('ec2', region_name='us-west-2',
                                aws_access_key_id=awsconfig.key,
                                aws_secret_access_key=awsconfig.secret)
        status = resource.describe_instance_status(InstanceIds=instances)
        if not status.get("InstanceStatuses"):
            print("Starting dump... Batman should wait aprox 30min to complete this asynchronous task...")
            print("To download this dump please use this command:")
            print("")
            print("--->>>> main.py get " + key + "_DD_MM_YY")
            print("")
            s3 = boto3.resource('s3', region_name='us-west-2',
                                aws_access_key_id=awsconfig.key,
                                aws_secret_access_key=awsconfig.secret)
            object = s3.Object('rankmi-backup-semanal', 'backup-type.dat')
            object.put(Body=key)
            resource.start_instances(InstanceIds=instances)
        else:
            print("Hay otro Dump en proceso, por favor intentende nuevo en unos minutos...")
    else:
        print('Batman, debes indicar el ambiente correctamente...')
