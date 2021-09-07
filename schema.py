from models import Channel
from pydantic import BaseModel


class User(BaseModel):
    first_name: str
    last_name: str = None
    age: int

    class Config:
        orm_mode = True


class Mobile(BaseModel):
    number: str

    class Config:
        orm_mode = True


class Message(BaseModel):
    message : str
    channel : int
    mobile : int

    class Config:
        orm_mode = True