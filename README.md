# alfred
Prerequisitos(el installer se encargará de ellos)
- python3
- pyenv
- pipenv
- pip3

## Instalación

``` sh 
$ sh installer.sh
# o puedes usar
$ ./installer.sh
```  


## Uso

### Credenciales
- La primera vez que la aplicación se ejecuta, la aplicación te solicitará las
  credenciales.
- En caso de que necesites modificar estas credenciales puedes hacerlo con el
  siguiente comando(si prefieres modificarla localmente, puedes modificar el
  archivo de configuración de alfred que está ubicado en ~/.alfred.conf):

``` sh 
  $ ./alfred reset credentials
```

### Descarga bases de datos
Fase 1: Copia de base de datos diaria a local

Las descargas se realizaran automaticamente en el directorio desde donde se ejecuta el script

- Para descargar la ultima db:
Ejemplo comando: `./alfred.sh get todaydb`

- Para descargar una db de un dia especifico: (Se debe usar el formato de fecha de la siguiente forma: YYYY_MM_DD)
ejemplo comando: `./alfred.sh get 2019_01_01`


Fase 2: Crear DUMP de la base de datos de cualquier ambiente (en pruebas):

- Para crear el dump:
``` sh 
./alfred.sh dump environment
```

Ejemplo: `./alfred.sh dump production`
