# alfred
Prerequisitos
- python3
- pip3

Instalar:

pip3 install boto3


Pruebas de funcionamiento:
- Se deben colocar las credenciales de AWS en el archivo alfred.conf
El formato del archivo es 

```
[AWS]
User=AWS_ACCESS_KEY
Pass=AWS_SECRET_KEY

[DIARIOS]
Bucket=nombre-del-bucket

```

Fase 1: Copia de base de datos diaria a local

- Para descargar la ultima db:
Ejemplo comando: `./alfred.py get todaydb /path/de/destino/nombre_de_archivo.tar.xz`

- Para descargar una db de un dia especifico: (Se debe usar el formato de fecha de la siguiente forma: YYYY_MM_DD)
ejemplo comando: `./alfred.py get 2019_01_01 /path/de/destino/nombre_de_archivo.tar.xz`
