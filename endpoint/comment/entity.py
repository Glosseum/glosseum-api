from pydantic import BaseModel


class CommentCreate(BaseModel):
    content: str = "Default Comment"

    class Config:
        orm_mode = True


class CommentUpdate(BaseModel):
    content: str = "Default Comment"

    class Config:
        orm_mode = True


class CommentGet(BaseModel):
    id: int
    content: str = "Default Comment"
    creator_id: int

    class Config:
        orm_mode = True
