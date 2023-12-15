from pydantic import BaseModel


class UserAuth(BaseModel):
    username: str
    password: str
