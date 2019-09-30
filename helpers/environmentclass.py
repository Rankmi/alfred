from dataclasses import dataclass

from mashumaro import DataClassDictMixin


@dataclass(frozen=True)
class Environment(DataClassDictMixin):
    """ Response serialization from kato service  """
    container_name: str
    container_ip: str
    database_name: str
    database_password: str
    database_port: int
    database_username: str
