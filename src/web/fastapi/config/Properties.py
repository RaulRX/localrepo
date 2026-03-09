from enum import Enum
import configparser
import os
#Local env file purpose
#from dotenv import load_dotenv, dotenv_values

#Local testing purposes
#load_dotenv()

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
        
        if Environment.LOCAL is Environment.get_environment_by_name(os.getenv("environment", Environment.LOCAL.name)):
            self.__config.read_file(open("application-standalone.ini"))
        else:
            self.__config.read_file(open("application-dev.ini"))

    def get_log_level(self):
        return f"{self.__config['log.level']}"
    
    def get_project_environment(self):
        return f"{self.__config['env']}"
    
    def get_property(self, name: str):
        if name.isspace():
            return None
        return self.__config.get(section=configparser.DEFAULTSECT, option=name)