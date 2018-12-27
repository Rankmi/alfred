#!/usr/bin/python3

# change above line to point to local 
# python executable

import boto3
import sys 
from configparser import ConfigParser
parser = ConfigParser()
parser.read('alfred.conf')

AUTHUSER=parser.get('AWS', 'User')
AUTHPASS=parser.get('AWS', 'Pass')
BUCKET=parser.get('AWS', 'Bucket')
COMANDO=str(sys.argv[1])
ARCHIVO=str(sys.argv[2])
PATH_DESTINO=str(sys.argv[3])

print ('el AUTHUSER  es ' + AUTHUSER)
print ('el AUTHPASS es ' + AUTHPASS)
print ('el bucket es ' + BUCKET)
print ('el archivo origen se llama ' + ARCHIVO)
print ('el path destino es ' + PATH_DESTINO)
print('')
if COMANDO == 'descargar':
    if ARCHIVO == 'dbdeldia':
        print ('Descaragando la db de hoy')
    else:
        print ('Descaragando la db ' + ARCHIVO)
    

#S3_OBJECT = boto3.client('s3', region_name='us-east-1', aws_access_key_id='AWS_ACCESS_KEY', aws_secret_access_key='AWS_SECRETY_KEY')

#s3.download_file(BUCKET,ARCHIVO,PATH_DESTINO)


