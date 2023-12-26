from pydantic import BaseModel


class ArticleCreate(BaseModel):
    title: str
    content: str

    class Config:
        orm_mode = True


class ArticleAppend(BaseModel):
    logic: str = "AGREE"
    title: str
    content: str

    class Config:
        orm_mode = True


class ArticleUpdate(BaseModel):
    title: str
    content: str

    class Config:
        orm_mode = True


class ArticleGet(BaseModel):
    title: str
    content: str
    creator_id: int
    path: str
    path_logical: str

    class Config:
        orm_mode = True
