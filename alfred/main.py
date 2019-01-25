#!/usr/bin/env python3

# change above line to point to local 
# python executable
import sys
import threading
from configparser import ConfigParser

import boto3
import botocore
import datetime
import getpass
from .alfredconfig import AlfredConfig
from .configfilehelper import config_file_exists, configlocation, set_config_file



def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '*' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

class ProgressPercentage(object):
    def __init__(self, client, bucket, filename):
        self._filename = filename
        s3 = boto3.client('s3', region_name='us-west-2', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        self._size = s3.head_object(Bucket=bucket, Key=filename)['ContentLength']
        self._seen_so_far = 0
        self._lock = threading.Lock()
    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = round((self._seen_so_far / self._size) * 100,2)
            if int(percentage) % 1 == 0:
                print_progress(int(percentage),100,"Downloading "+filename,"Completed",0,int(percentage))


# Asking for user access keys
if config_file_exists():
    parser = ConfigParser()
    parser.read(configlocation)
    AWS_ACCESS_KEY=parser.get('AWS', 'User')
    AWS_SECRET_KEY=parser.get('AWS', 'Pass')
    BUCKET = parser.get('DIARIOS', 'Bucket')
else:
    AWS_ACCESS_KEY = input('User: ')
    AWS_SECRET_KEY = getpass.getpass('Password: ')
    BUCKET = input('Bucket (default = rankmi-backup-semanal) : ')
    if not BUCKET:
        BUCKET = 'rankmi-backup-semanal'
    set_config_file(AlfredConfig(AWS_ACCESS_KEY, AWS_SECRET_KEY, BUCKET))



#INICIALIZANDO VARIABLES
COMANDO=str(sys.argv[1])
KEY=str(sys.argv[2])

#IMPRIMIR VARIABLES
filename = KEY

#SELECCION DE PROCESO



#PROCESO GET
if COMANDO == 'get':
    resource = boto3.resource('s3', region_name='us-west-2', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    
    if KEY == 'todaydb':
        filename = datetime.datetime.now().strftime('%Y_%m_%d')
    
    print ('Download  '+filename+' database')
    progress = ProgressPercentage(resource, BUCKET, 'backup_reducido_' + filename + '.tar.xz')    
    try:
        resource.Bucket(BUCKET).download_file('backup_reducido_' + filename + '.tar.xz','backup_reducido_' + KEY + '.tar.gz',Callback=progress)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("There's no database... Try with the following format YYYY_MM_DD")
        else:
            raise


#PROCESO DUMP
elif COMANDO == 'dump':
    if (KEY == 'production') or (KEY == 'staging') or (KEY == 'development'):
        #revisar si la maquina esta encendida, si lo esta solicitar intentar nuevamente, sino lo esta entonces encender
        print ('Batman, the dump of the '+KEY+' environment is starting...')
        instances = ['i-0b08005bfb8829080']
        resource = boto3.client('ec2', region_name='us-west-2', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        status=resource.describe_instance_status(InstanceIds=instances)
        if not status.get("InstanceStatuses"):
            print("Starting dump... Batman should wait aprox 30min to complete this asynchronous task...")
            print("To download this dump please use this command:")
            print("")
            print("--->>>> main.py get "+KEY+"_DD_MM_YY")
            print("")
            s3 = boto3.resource('s3', region_name='us-west-2', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
            object = s3.Object('rankmi-backup-semanal','backup-type.dat')
            object.put(Body=KEY)
            resource.start_instances(InstanceIds=instances)
        else:
            print ("Hay otro Dump en proceso, por favor intentende nuevo en unos minutos...")

    else:
        print ('Batman, debes indicar el ambiente correctamente...')

else:
    print ('Command Unknown. Maybe you could try with get command')
