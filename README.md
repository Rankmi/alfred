# alfred
Prerequisitos
- python3
- pip3

Instalar:

pip3 install boto3


Pruebas de funcionamiento:
- Se deben colocar las credenciales de AWS en el archivo alfred.conf

Fase 1: Copia de base de datos diaria a local
- Para descargar la ultima db:
comando: ./alfred.py descargar dbdia /path/de/destino

-Para descargar una db de un dia especifico:
Se debe usar el formato de fecha de la siguiente forma: YYYY_MM_DD
comando: ./alfred.py descargar 2019_01_01 /path/de/destino
