from pydantic import BaseModel

class Greeting_request(BaseModel):
    name: str = "world"
    surname : str = ""
    detail: str = ""