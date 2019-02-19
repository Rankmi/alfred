# alfred

- [Descarga](#descarga)
- [Instalación](#instalación)
- [Uso](#uso)
    - [Credenciales](#credenciales)
    - [AWS](#aws)
    - [GitHub](#github)
    - [YouTrack](#youtrack)

### Descarga

Para encontrar la útlima versión de **alfred**, puedes revisar la lista de [Releases](https://github.com/Rankmi/alfred/releases) y descargar la versión correspondiente a tu sistema operativo.

### Instalación

**alfred** es un archivo ejecutable, por lo que si deseas acceder a él desde cualquier lugar, debes guardar el archivo en cualquier carpeta `bin` (por ejemplo: `/usr/local/bin`). De lo contrario, solo podrás utilizarlo estando en el directorio donde se encuentre.

## Uso

### Credenciales

La primera vez que la aplicación se ejecuta, la aplicación te solicitará las credenciales.

En caso de que necesites modificar las credenciales de algún servicio, puedes hacerlo con el siguiente comando:

``` bash 
 # Los servicios pueden ser: aws, github, youtrack, all 
 $ alfred reset <service>
```

### AWS

#### Descarga de DB

Si deseas descargar una base de datos desde AWS puedes: 

Descargar la última base de datos:
``` bash
 # Si deseas descargar la base de datos del día correspondiente, usa 'todaydb' como fecha
 # En otro caso, el día debe estar en formato YYYY_MM_DD
 $ alfred get <date> [--extract    # Descomprimir el archivo una vez terminada la descarga]
``` 

#### Realizar Dump en un ambiente

Para realizar un Dump de la base de datos dentro de un ambiente debes ejecutar:
``` bash 
 # Los ambientes pueden ser: production, staging, development
 $ alfred dump <environment>
```

### GitHub

#### Crear Branches

La creación de una rama depende del repositorio en donde se creará y cual será su base, por lo que se debe ejecutar el
siguiente comando:
``` bash
 # Por defecto, la rama se creará desde 'development'
 $ alfred branch <repository> <name> [-h    # Para crear la rama desde 'master']
```

#### Crear Pull Requests

Nuevamente, debemos especificar en que repositorio queremos crear el Pull request, qué rama usar y hacia donde mergear:

``` bash
 # Por defecto, el Pull request será dirigido a 'development' y tendrá el mismo título de la rama 
 $ alfred pr <repository> -r <branch-name> [-t <title>  # Para agregar un título]
                                           [-h          # Para dirigir el merge a 'master']
```

#### Crear Repositorios

Puedes crear un repositorio privado en Rankmi ejecutando:
``` bash
 $ alfred repo <name>
```

### YouTrack

#### Revisar tickets abiertos

Para obtener una lista de los tickets por resolver puedes usar:
``` bash
 $ alfred tasks open
``` 

#### Revisar un ticket por ID

A partir de la ID de un ticket, recibirás información relevante sobre la tarea. Para hacerlo utiliza el comando:
``` bash
 # La ID puede ser en formato RKM-XXXX o solo XXXX
 $ alfred issue <ID>
```