from pydantic import BaseModel, constr, validator, ValidationError, Field, field_validator
from enum import Enum


class ArticleLogic(str, Enum):
    AGREE = "AGREE"
    DISAGREE = "DISAGREE"
    NEUTRAL = "NEUTRAL"


class ArticleCreate(BaseModel):
    name: str
    content: str

    class Config:
        orm_mode = True


class ArticleAppend(BaseModel):
    id: int
    logic: ArticleLogic
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
    path_logical: constr(to_upper=True)

    @field_validator("path_logical")
    def path_logical_validator(cls, logic: str):
        for logic in logic.split("/"):
            if logic not in ArticleLogic.__members__:
                raise ValidationError(f"{logic}는 잘못된 경로입니다.")
        return logic

    class Config:
        orm_mode = True
