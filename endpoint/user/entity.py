"""
유저의 입출력 형식(스키마)을 정의합니다.
"""

from pydantic import BaseModel


class UserCreate(BaseModel):
    """
    유저를 생성할 때에는 사용자명, 이메일, 비밀번호 1, 비밀번호 2를 입력받습니다.
    """

    username: str
    email: str = "email@email.com"
    password1: str
    password2: str

    class Config:
        """
        SQLAlchemy의 ORM Model 형태의 데이터를 Pydantic 모델로 변환합니다.
        """

        orm_mode = True


class UserUpdate(BaseModel):
    """
    유저를 수정할 때에는 사용자명, 이메일을 입력받습니다.
    """

    username: str
    email: str = "email@email.com"

    class Config:
        """
        SQLAlchemy의 ORM Model 형태의 데이터를 Pydantic 모델로 변환합니다.
        """

        orm_mode = True


class UserGet(BaseModel):
    """
    특정 유저를 조회할 때에는 id, 사용자명, 이메일을 출력합니다.
    """

    id: int
    username: str
    email: str = "email@email.com"

    class Config:
        """
        SQLAlchemy의 ORM Model 형태의 데이터를 Pydantic 모델로 변환합니다.
        """

        orm_mode = True


class Token(BaseModel):
    """
    로그인 했을 때 반환되는 토큰의 형식을 정의합니다.
    """

    access_token: str
    token_type: str
    username: str
