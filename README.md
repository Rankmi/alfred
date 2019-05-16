# alfred

- [Descarga](#descarga)
- [Instalación](#instalación)
- [Uso](#uso)
    - [Credenciales](#credenciales)
    - [Flujo de desarrollo](#flujo-de-desarrollo)
    - [AWS](#aws)
    - [GitHub](#github)
    - [YouTrack](#youtrack)
    
### Descarga

Para encontrar la útlima versión de **alfred**, puedes revisar la lista de [Releases](https://github.com/Rankmi/alfred/releases) y descargar la versión correspondiente a tu sistema operativo.

### Instalación

Para acceder a **alfred** desde cualquier directorio, debes posicionarlo en `/usr/local/bin`

``` console
$ mv /path/to/alfred /usr/local/bin/
```

## Uso

### Credenciales

La primera vez que la aplicación se ejecuta, la aplicación te solicitará las credenciales.

En caso de que necesites modificar las credenciales de algún servicio, puedes hacerlo con el siguiente comando:

``` console 
 # Los servicios pueden ser: aws, github, youtrack, all 
 $ alfred reset <service>
```
#### Credenciales Github:
Para obtener el token de github se debe ir a Settings -> Developer settings -> Personal access tokens y generar un token nuevo.

#### Credenciales AWS:
Conversar con el devops

#### Credenciales Youtrack
Solicitar con el devops


### Flujo de desarrollo

Al realizar acciones que involucren el uso de Gitflow, debes utilizar: 
- `alfred start feature <RKM-XXXX>`: A través de Gitflow, alfred creará la rama de desarrollo y automáticamnte actualizará
el estado de la tarea en YouTrack a 'En Progreso'. 

- `alfred finish feature <RKM-XXXX>`: Se creará un Pull request en GitHub y se agregará su enlace a la descripción de la tarea en YouTrack. 
Cambiará el estado de la tarea a 'Para CodeReview', cambiará tu rama a 'development' y descargará sus últimos cambios.  

- `alfred close feature <RKM-XXXX>`: Cambiará el estado de la tarea a 'Aceptado' o 'Producción' según corresponda, cambiará tu rama a 
'development' y descargará sus últimos cambios. Además, eliminará la rama de desarrollo.
*El Pull-Request asociado a la rama debe estar Mergeado para realizar esta acción*

* Para Hotfixes, debes utilizar el versionamiento con formato X.Y.ISSUE_ID (sin RKM-). Por ejemplo: `alfred start hotfix 3.10.6346`.

Para las siguientes opciones, tu rama activa deberá comenzar con 'RKM-XXXX':

- `alfred task qa`: Cambiará el estado de la tarea a 'Pendiente de QA', cambiará tu rama a 'development' y descargará sus últimos
cambios.

- `alfred task changes`: Cambiará el estado de la tarea a 'CR Cambios Solicitados', cambiará tu rama a 'development' y descargará 
sus últimos cambios.

- `alfred task review`: Cambiará el estado de la tarea a 'En Review'.

- `alfred task reject`: Cambiará el estado de la tarea a 'Rechazado', cambiará tu rama a 'development' y descargará 
sus últimos cambios.

### YouTrack

#### Revisar tickets por estado

Para obtener una lista de los tickets por resolver puedes usar:
``` console
 # Estados: all, pending, progress, cr, changes, qa, accepted o rejected.  
 $ alfred tasks <state>
``` 

#### Revisar un ticket por ID

A partir de la ID de un ticket, recibirás información relevante sobre la tarea. Para hacerlo utiliza el comando:
``` console
 # La ID puede ser en formato RKM-XXXX o solo XXXX
 $ alfred issue <ID>
```

### AWS

#### Descarga de DB

Si deseas descargar una base de datos desde AWS puedes: 

Descargar la última base de datos:
``` console
 # Si deseas descargar la base de datos del día correspondiente, usa 'todaydb' como fecha
 # En otro caso, el día debe estar en formato YYYY_MM_DD
 $ alfred get <date> [--extract    # Descomprimir el archivo una vez terminada la descarga]
                     [--delete     # Eliminar el archivo .tar luego de descomprimirse]
``` 

#### Realizar Dump en un ambiente

Para realizar un Dump de la base de datos dentro de un ambiente debes ejecutar:
``` console 
 # Los ambientes pueden ser: production, staging, development
 $ alfred dump <environment>
```

### GitHub

#### Crear Branches

La creación de una rama depende del repositorio en donde se creará y cual será su base, por lo que se debe ejecutar el
siguiente comando:
``` console
 # Por defecto, la rama se creará desde 'development'
 $ alfred branch <repository> <name> [-h    # Para crear la rama desde 'master']
```

#### Crear Pull Requests

Nuevamente, debemos especificar en que repositorio queremos crear el Pull request, qué rama usar y hacia donde mergear:

``` console
 # Por defecto, el Pull request será dirigido a 'development' y tendrá el mismo título de la rama 
 $ alfred pr <repository> -r <branch-name> [-t <title>  # Para agregar un título]
                                           [-h          # Para dirigir el merge a 'master']
```

#### Crear Repositorios

Puedes crear un repositorio privado en Rankmi ejecutando:
``` console
 $ alfred repo <name>
```
