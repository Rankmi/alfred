from pathlib import Path
import os
import configparser


__configfilename = '.alfred.conf'
configlocation = Path(os.path.join(Path.home(), __configfilename))


def config_file_exists():
    if configlocation.is_file():
        return True
    else:
        return False


def set_config_file(userconfig):
    config = configparser.ConfigParser()
    config.optionxform = str
    config['AWS'] = {}
    config['AWS']['User'] = userconfig.user
    config['AWS']['Pass'] = userconfig.password
    config['DIARIOS'] = {}
    config['DIARIOS']['Bucket'] = userconfig.bucket
    with open(configlocation, "w+") as file:
        config.write(file)
        print("Creando archivo")

