from pydantic import BaseModel


class ArticleCreate(BaseModel):
    name: str
    content: str

    class Config:
        orm_mode = True


class ArticleAppend(BaseModel):
    id: int
    logic: str = "AGREE"
    name: str
    content: str

    class Config:
        orm_mode = True


class ArticleUpdate(BaseModel):
    name: str
    content: str

    class Config:
        orm_mode = True


class ArticleGet(BaseModel):
    id: int
    name: str
    content: str
    creator_id: int
    path: str
    path_logical: str

    class Config:
        orm_mode = True
