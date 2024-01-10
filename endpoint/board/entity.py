"""
불판의 입출력 형식(스키마)을 정의합니다.
불판 : Board, 장작 : Article
"""

from pydantic import BaseModel


class BoardCreate(BaseModel):
    """
    불판을 생성할 때에는 제목과 상세 설명을 입력받습니다.
    """

    name: str
    description: str = "Board Description"

    class Config:
        """
        SQLAlchemy의 ORM Model 형태의 데이터를 Pydantic 모델로 변환합니다.
        """

        orm_mode = True


class BoardUpdate(BaseModel):
    """
    불판을 수정할 때에는 제목과 상세 설명을 입력받습니다.
    """

    name: str
    description: str = "Board Description"

    class Config:
        """
        SQLAlchemy의 ORM Model 형태의 데이터를 Pydantic 모델로 변환합니다.
        """

        orm_mode = True


class BoardGet(BaseModel):
    """
    불판을 조회할 때에는 id와 제목, 상세 설명을 출력합니다.
    """

    id: int
    name: str
    description: str = "Board Description"

    class Config:
        """
        SQLAlchemy의 ORM Model 형태의 데이터를 Pydantic 모델로 변환합니다.
        """

        orm_mode = True
