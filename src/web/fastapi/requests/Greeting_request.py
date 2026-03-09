from pydantic import BaseModel
from typing import Optional

class Greeting_request(BaseModel):
    name: str = "world"
    surname : str = ""
    detail: Optional[str]