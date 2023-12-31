from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str = "email@email.com"
    password1: str
    password2: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: str
    email: str = "email@email.com"

    class Config:
        orm_mode = True


class UserGet(BaseModel):
    username: str
    email: str = "email@email.com"

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
