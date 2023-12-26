from pydantic import BaseModel


class BoardCreate(BaseModel):
    name: str
    description: str = "Board Description"

    class Config:
        orm_mode = True


class BoardUpdate(BaseModel):
    name: str
    description: str = "Board Description"

    class Config:
        orm_mode = True


class BoardGet(BaseModel):
    id: int
    name: str
    description: str = "Board Description"

    class Config:
        orm_mode = True
