from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from endpoint.user.service import register_user, get_current_user, update_current_user, verify_user, delete_current_user
from endpoint.user.entity import UserGet, UserCreate, UserUpdate, Token
from endpoint.user.repository import User


router = APIRouter(
    prefix="/user"
)


@router.post("/register", status_code=status.HTTP_204_NO_CONTENT)
async def register(_user_create: UserCreate):
    await register_user(
        _user_create.username,
        _user_create.email,
        _user_create.password1,
        _user_create.password2
    )


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    access_token = await verify_user(form_data.username,
                                     form_data.password)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": form_data.username
    }


@router.get("/me", response_model=UserGet)
async def get_user_me(user: User = Depends(get_current_user)) -> UserGet:
    return user  # 추후 작성 게시글 모아 보기 등도 추가..


@router.put("/{username}")
async def update_user(_user_update: UserUpdate, user: User = Depends(get_current_user)) -> None:
    return await update_current_user(
        username_original=user.username,
        username_to_update=_user_update.username,
        email_to_update=_user_update.email
    )


@router.delete("/{username}")
async def delete_user(user: User = Depends(get_current_user)) -> None:
    return await delete_current_user(user.username)
