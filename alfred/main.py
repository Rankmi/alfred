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
from alfredconfig import AlfredConfig
from configfilehelper import config_file_exists, configlocation, set_config_file
from tqdm import tqdm

AWS_ACCESS_KEY = ""
AWS_SECRET_KEY = ""
BUCKET = ""

#SELECCION DE PROCESO
def parsearguments(command, key):
    #PROCESO GET
    if command == 'get':
        getbackup(key, AWS_ACCESS_KEY, AWS_SECRET_KEY, BUCKET)
    #PROCESO DUMP
    elif command == 'dump':
        dumpbackup(key, AWS_ACCESS_KEY, AWS_SECRET_KEY, BUCKET)
    #RESET CREDENTIALS
    elif command == 'reset':
        if key == 'credentials':
            askcredentials()
    else:
        print ('Command Unknown. Maybe you could try with get command')

# Validación de largo de argumentos
def validateargv():
    if len(sys.argv) == 3:
        global FILENAME
        COMANDO=str(sys.argv[1])
        KEY=str(sys.argv[2])
        FILENAME = KEY
        parsearguments(COMANDO, KEY)
    else:
        print("Debes ingresar al menos dos argumentos")



def askcredentials():
    AWS_ACCESS_KEY = input('User: ')
    AWS_SECRET_KEY = getpass.getpass('Password: ')
    BUCKET = input('Bucket (default = rankmi-backup-semanal) : ')
    if not BUCKET:
        BUCKET = 'rankmi-backup-semanal'
    set_config_file(AlfredConfig(AWS_ACCESS_KEY, AWS_SECRET_KEY, BUCKET))


def hook(t):
  def inner(bytes_amount):
    t.update(bytes_amount)
  return inner

def getbackup(key, awskey, awssecret, bucket):
    resource = boto3.resource('s3', region_name='us-west-2', aws_access_key_id=awskey, aws_secret_access_key=awssecret)
    if key == 'todaydb':
        filename = datetime.datetime.now().strftime('%Y_%m_%d')

    print ('Download ' + filename + ' database')
    awsfile = 'backup_reducido_' + filename + '.tar.xz'
    fileobject = resource.Object(bucket, awsfile)
    filesize = fileobject.content_length
    try:
        FILE_NAME = "algo"
        with tqdm(total=filesize, unit='B', unit_scale=True, desc=FILE_NAME) as t:
            resource.Bucket(bucket).download_file(awsfile, 'backup_reducido_' + key + '.tar.gz',Callback=hook(t))
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("There's no database... Try with the following format YYYY_MM_DD")
        else:
            raise

def dumpbackup(key, awssecret, bucket):
    if (key == 'production') or (key == 'staging') or (key == 'development'):
        #revisar si la maquina esta encendida, si lo esta solicitar intentar nuevamente, sino lo esta entonces encender
        print ('Batman, the dump of the '+key+' environment is starting...')
        instances = ['i-0b08005bfb8829080']
        resource = boto3.client('ec2', region_name='us-west-2', aws_access_key_id=awskey, aws_secret_access_key=awssecret)
        status=resource.describe_instance_status(InstanceIds=instances)
        if not status.get("InstanceStatuses"):
            print("Starting dump... Batman should wait aprox 30min to complete this asynchronous task...")
            print("To download this dump please use this command:")
            print("")
            print("--->>>> main.py get "+key+"_DD_MM_YY")
            print("")
            s3 = boto3.resource('s3', region_name='us-west-2', aws_access_key_id=awskey, aws_secret_access_key=awssecret)
            object = s3.Object('rankmi-backup-semanal','backup-type.dat')
            object.put(Body=key)
            resource.start_instances(InstanceIds=instances)
        else:
            print ("Hay otro Dump en proceso, por favor intentende nuevo en unos minutos...")

    else:
        print ('Batman, debes indicar el ambiente correctamente...')

def readconfig():
    global AWS_ACCESS_KEY, AWS_SECRET_KEY, BUCKET
    parser = ConfigParser()
    parser.read(configlocation)
    AWS_ACCESS_KEY=parser.get('AWS', 'User')
    AWS_SECRET_KEY=parser.get('AWS', 'Pass')
    BUCKET = parser.get('DIARIOS', 'Bucket')

if __name__ == '__main__':
    if config_file_exists():
        readconfig()
    else:
        askcredentials()
    FILENAME = "default"
    validateargv()
