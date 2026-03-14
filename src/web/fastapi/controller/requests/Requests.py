from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator
from typing import Optional
import re

class Message_req(BaseModel):
   user: str = Field(..., description="Name of the user")
   user_id: str = Field(..., alias = "userId", description="User identification name")
   chain: str = Field(..., alias = "content", description="Message content")

   @field_validator("user_id")
   def is_nif_or_nie(cls, userId):
      DNI_NIE_PATTERN = re.compile(r'^(?:[0-9]{8}|[XYZ][0-9]{7})[A-Z]$')
      if not userId.isalnum() or bool(DNI_NIE_PATTERN.match(userId)) is False:
         raise ValueError("User ID is not valid")
      return userId
      
   @field_validator("user")
   def user_long(cls, user):
      if len(user) > 64:
         raise ValueError("User name lenght is not valid")
      return user
      
   @field_validator("chain")
   def content_long(cls, content):
      if len(content) > 255:
         raise ValueError("message content is not valid")
      return content

class Greeting_request(BaseModel):
    name: str = Field(default = "world", alias="firstName", description="Person name that saludate", min_length=0, max_length=16)
    surname: str = Field(default = '', alias="lastName", min_length=0, max_length=64)
    detail: Optional[str] = Field(default = None, alias="description", min_length=0, max_length=255)

    @model_validator(mode='before')
    def validate_before_call(cls, data: dict):
       name = data['firstName']
       surname = data['lastName']
       
       if not isinstance(name, str) and not isinstance(surname, str):
          raise ValueError("firstName and lastName must be a chain of characters")
       
       if name == surname:
          raise ValidationError("firstName and lastName must not be sent with same value")

       for key, value in data.items():
           if key in ['firstName', 'lastName'] and not isinstance(value, str):
               raise ValueError("firstName or lastName fields must be a String")
           data[key] = data[key].strip()

    @field_validator("name", "surname", "detail")
    def valid_surname(cls, value):
       if value is not None and not value.isspace():
          if not any(vowel in value for vowel in ['a', 'e', 'i', 'o', 'u']):
            raise ValueError("Lastname must contain at least one vowel")
       
       return value
           

    #Validate model after all field validators are executed
    @model_validator(mode='after')
    def valid_name_surname(cls, instance):
       if instance.name.lower() == 'world':
           instance.surname = "!!!"
       
       return instance
    
   