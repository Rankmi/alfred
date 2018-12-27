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
ARCHIVO=str(sys.argv[1])
PATH_DESTINO=str(sys.argv[2])

print ('el AUTHUSER  es ' + AUTHUSER)
print ('el AUTHPASS es ' + AUTHPASS)
print ('el bucket es ' + BUCKET)
print ('el archivo origen se llama ' + ARCHIVO)
print ('el path destino es ' + PATH_DESTINO)

#S3_OBJECT = boto3.client('s3', region_name='us-east-1', aws_access_key_id='AWS_ACCESS_KEY', aws_secret_access_key='AWS_SECRETY_KEY')

#s3.download_file(BUCKET,ARCHIVO,PATH_DESTINO)


