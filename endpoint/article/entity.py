"""
장작의 입출력 형식(스키마)을 정의합니다.
불판 : Board, 장작 : Article
"""

from enum import Enum
from pydantic import BaseModel, constr, ValidationError, field_validator


class ArticleLogic(str, Enum):
    """
    장작에 찬성, 반대, 중립의 반응(로직)을 남길 수 있습니다.
    """

    AGREE = "AGREE"
    DISAGREE = "DISAGREE"
    NEUTRAL = "NEUTRAL"

    def __str__(self):
        return str(self.value)

class ArticleCreate(BaseModel):
    """
    장작을 처음 생성할 때 입력받는 정보입니다.
    제목, 내용을 입력받습니다.
    """

    name: str
    content: str

    class Config:
        """
        SQLAlchemy의 ORM Model 형태의 데이터를 Pydantic 모델로 변환합니다.
        """

        orm_mode = True


class ArticleAppend(BaseModel):
    """
    장작을 추가할 때 입력받는 정보입니다.
    id, 반응(로직), 제목, 내용을 입력받습니다.
    """

    logic: ArticleLogic
    name: str
    content: str

    class Config:
        """
        SQLAlchemy의 ORM Model 형태의 데이터를 Pydantic 모델로 변환합니다.
        """

        orm_mode = True


class ArticleUpdate(BaseModel):
    """
    장작을 수정할 때 입력받는 정보입니다.
    제목과 내용을 입력받습니다.
    """

    name: str
    content: str

    class Config:
        """
        SQLAlchemy의 ORM Model 형태의 데이터를 Pydantic 모델로 변환합니다.
        """

        orm_mode = True


class ArticleGet(BaseModel):
    """
    장작을 조회할 때 출력하는 정보입니다.
    id, 제목, 내용, 생성자 id, 이전 장작, 이전 장작에 대한 반응을 포함하고 있습니다.
    """

    id: int
    name: str
    content: str
    creator_id: int
    path: str
    path_logical: constr(to_upper=True)

    # @field_validator("path_logical")
    # def path_logical_validator(self, logic: str):
    #     """
    #     반응(로직)이 ArticleLogic의 3개 멤버중 하나에 속하는지 검증합니다.
    #     """

    #     for _logic in logic.split("/"):
    #         if _logic not in ArticleLogic.__members__:
    #             raise ValidationError(f"{logic}는 잘못된 경로입니다.")
    #     return logic

    class Config:
        """
        SQLAlchemy의 ORM Model 형태의 데이터를 Pydantic 모델로 변환합니다.
        """

        orm_mode = True
