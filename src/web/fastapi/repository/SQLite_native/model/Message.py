from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import re


@dataclass(kw_only=True)
class Message:
    user: str
    user_id: str
    updated_date: datetime
    chain: str
    created_date: Optional[datetime] = datetime.now()
    id: Optional[int] = None

    def __post_init__(self):
        self.__valid_user_id()


    def __valid_user_id(self):
        if not Dni_Nie_Validator.is_dni_nie_valid(self.user_id):
            raise ValueError("User ID must be a valid identification number")

class Dni_Nie_Validator:

    _DNI_NIE_PATTERN = re.compile(r'^(?:[0-9]{8}|[XYZ][0-9]{7})[A-Z]$')

    @staticmethod
    def is_dni_nie_valid(value) -> bool:
        return bool(Dni_Nie_Validator._DNI_NIE_PATTERN.match(value))
    