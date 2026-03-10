from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional

class Greeting_request(BaseModel):
    name: str = Field(default = "world", description="Person name that saludate", min_length=0, max_length=16) 
    surname : str = Field(alias="lastname") # ... indicates its mandatory
    detail: Optional[str] = Field(default = None)

    @field_validator("surname")
    def valid_surname(cls, value):
       if not any(vowel in value for vowel in ['a', 'e', 'i', 'o', 'u']):
           raise ValueError("Lastname must contain at least one vowel")
       
       return value
    
    #Validate model after all field validators are executed
    @model_validator(mode='after')
    def valid_name_surname(cls, instance):
       if instance.name == 'WORLD'.lower() and instance.surname.isspace():
           instance.surname = "!!!"
       
       return instance