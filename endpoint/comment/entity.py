"""
댓글의 입출력 형식(스키마)을 정의합니다.
"""

from pydantic import BaseModel


class CommentCreate(BaseModel):
    """
    댓글을 생성할 때에는 내용을 입력받습니다.
    """

    content: str = "Default Comment"

    class Config:
        """
        SQLAlchemy의 ORM Model 형태의 데이터를 Pydantic 모델로 변환합니다.
        """

        orm_mode = True


class CommentUpdate(BaseModel):
    """
    댓글을 수정할 때에는 내용을 입력받습니다.
    """

    content: str = "Default Comment"

    class Config:
        """
        SQLAlchemy의 ORM Model 형태의 데이터를 Pydantic 모델로 변환합니다.
        """

        orm_mode = True


class CommentGet(BaseModel):
    """
    댓글을 조회할 때에는 id와 내용, 작성자를 출력합니다.
    """

    id: int
    content: str = "Default Comment"
    creator_id: int

    class Config:
        """
        SQLAlchemy의 ORM Model 형태의 데이터를 Pydantic 모델로 변환합니다.
        """

        orm_mode = True
