from enum import Enum

class Status(Enum):
    OK = 200
    BAD_REQUEST = 400
    NOT_FOUND = 404
    ERROR = 500

    def get_value(self) -> int:
        return self.value;