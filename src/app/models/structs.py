import typing

from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    

class BearerStructure(BaseModel):
    refresh_token: typing.Optional[str]
