from enum import Enum
import configparser
import os
#Local env file purpose
#from dotenv import load_dotenv, dotenv_values

#Local testing purposes
#load_dotenv(dotenv_path="../../../config/.env")

class Environment(Enum):
    LOCAL="local",
    DEV = "dev",
    BETA = "pre",
    PRO = "pro"

    @staticmethod
    def get_environment_by_name(name: str = "local"):
        return (member for member in Environment if member.value == name.lower()) or None
    
class Common:

    def __init__(self):
        self.__config = configparser.ConfigParser()
        env = os.getenv("environment", Environment.LOCAL.name)
        print(f"env: {env}")
        print(f"Environment value: {'wrong environment' if env == 'LOCAL' else env}")
        if Environment.LOCAL is Environment.get_environment_by_name(env):
            self.__config.read_file(open("resources/application-standalone.ini"))
        else:
            self.__config.read_file(open("resources/application-dev.ini"))
    
    def get_property(self, name: str):
        if name.isspace():
            return None
        return self.__config.get(section=configparser.DEFAULTSECT, option=name)