"""
유저와 관련된 모든 라우팅 경로 URL을 정의합니다.
"""

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from endpoint.user.service import (
    verify_univ,
    register_user,
    get_current_user,
    update_current_user,
    verify_user,
    delete_current_user,
)
from endpoint.user.entity import UnivVerify, UserGet, UserCreate, UserUpdate, Token
from endpoint.user.repository import User


router = APIRouter(prefix="/user")

@router.post("/univ_verify", status_code=status.HTTP_204_NO_CONTENT, tags=["User"])
async def univ_verify(_univ_verify: UnivVerify):
    """
    유저의 대학교 이메일에 인증 코드를 전송할 때의 라우팅 경로를 정의합니다.
    """
    await verify_univ(
        _univ_verify.email
    )

@router.post("/register", status_code=status.HTTP_204_NO_CONTENT, tags=["User"])
async def register(_user_create: UserCreate):
    """
    유저를 생성(회원가입)할 때의 라우팅 경로를 정의합니다.
    """
    await register_user(
        _user_create.username,
        _user_create.email,
        _user_create.code,
        _user_create.password1,
        _user_create.password2,
    )


@router.post("/login", response_model=Token, tags=["User"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    로그인 할때의 라우팅 경로를 정의합니다.
    유저의 정보를 검증한 후, 토큰을 반환합니다.
    """
    access_token = await verify_user(form_data.username, form_data.password)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": form_data.username,
    }


@router.get("/me", response_model=UserGet, tags=["User"])
async def get_user_me(user: User = Depends(get_current_user)) -> UserGet:
    """
    로그인한 유저의 정보를 반환합니다.
    """
    return user  # 추후 작성 게시글 모아 보기 등도 추가..


@router.put("/{username}", tags=["User"])
async def update_user(
    _user_update: UserUpdate, user: User = Depends(get_current_user)
) -> None:
    """
    유저의 정보를 수정할 때의 라우팅 경로를 정의합니다.
    """
    return await update_current_user(
        username_original=user.username,
        username_to_update=_user_update.username,
        email_to_update=_user_update.email,
    )


@router.delete("/{username}", tags=["User"])
async def delete_user(user: User = Depends(get_current_user)) -> None:
    """
    유저를 삭제할 때의 라우팅 경로를 정의합니다.
    """
    return await delete_current_user(user.username)
