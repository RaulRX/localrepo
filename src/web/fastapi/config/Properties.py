from enum import Enum
import configparser
import os
from pathlib import Path

class Environment(Enum):
    LOCAL="local",
    DEV = "dev",
    BETA = "pre",
    PRO = "pro"

    @staticmethod
    def get_by_name(name: str = "local"):
        return next((env for env in Environment if env if env.value == name.lower()), Environment.LOCAL)

    @classmethod
    def local_environment(cls, environment) -> bool:
        return cls.LOCAL == environment

class Common:

    def __init__(self):
        self.__config = configparser.ConfigParser()
        envvar = os.getenv("environment")
        if envvar is None:
            print(f"environment property not found: using LOCAL environment")
            envvar = Environment.LOCAL.name

        print(f"env: {envvar}")
        config_file = self.__get_configuration_file(envvar)
        print(f"file: {config_file}")
        self.__config.read_file(open(config_file))

    def __get_configuration_file(self, environment):
        return "src/web/fastapi/resources/application-dev.ini" if environment != Environment.LOCAL.name.lower() else "src/web/fastapi/resources/application-standalone.ini"
    
    def get_property(self, name: str):
        if name.isspace():
            return None
        return self.__config.get(section=configparser.DEFAULTSECT, option=name)