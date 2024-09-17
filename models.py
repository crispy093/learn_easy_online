from typing import Optional

from pydantic import BaseModel

class User(BaseModel):
    name: str
    password: str
    phone_number: str
    age: str

class ReturnableUser(BaseModel):
    name: str
    phone_number: str
    age: str

class Course(BaseModel):
    title: str
    description: str
    is_advanced: bool
    price: Optional[float] = None