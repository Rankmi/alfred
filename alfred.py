#!/usr/bin/python3

# change above line to point to local 
# python executable

import boto3
import botocore
import sys 
from configparser import ConfigParser
parser = ConfigParser()
parser.read('alfred.conf')

#INICIALIZANDO VARIABLES
AWS_ACCESS_KEY=parser.get('AWS', 'User')
AWS_SECRET_KEY=parser.get('AWS', 'Pass')
BUCKET=parser.get('DIARIOS', 'Bucket')
COMANDO=str(sys.argv[1])
KEY=str(sys.argv[2])
PATH_DESTINO=str(sys.argv[3])

#IMPRIMIR VARIABLES
print ('el AUTHUSER  es ' + AWS_ACCESS_KEY)
print ('el AUTHPASS es ' + AWS_SECRET_KEY)
print ('el bucket es ' + BUCKET)
print ('el archivo origen se llama ' + KEY)
print ('el path destino es ' + PATH_DESTINO)
print('')

#SELECCION DE PROCESO
if COMANDO == 'get':
    if KEY == 'todaydb':
        print ('Buscando y Descaragando la db de hoy')
        #Buscar la db mas reciente por fecha

    else:
        print ('Buscando y Descaragando la db backup_reducido_' + KEY + '.tar.xz')
        resource = boto3.resource('s3', region_name='us-west-2', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        try:
            resource.Bucket(BUCKET).download_file('backup_reducido_' + KEY + '.tar.xz', PATH_DESTINO)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("No existen db en esa fecha... pruebe nuevamente cambiando la fecha con formato YYYY_MM_DD")
            else:
                raise

elif COMANDO == 'crearlinkdiario':
    print ('Crear link')
else:
    print ('Comando desconocido')

#COMANDO DE LIBRERIA BOTO3 PARA DESCARGAR ARCHIVO


