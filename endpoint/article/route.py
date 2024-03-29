"""
장작과 관련된 모든 라우팅 경로 URL을 정의합니다.
"""

from fastapi import APIRouter, Depends, status

from endpoint.article import service
from endpoint.article.entity import (
    ArticleCreate,
    ArticleAppend,
    ArticleUpdate,
    ArticleGet,
)
from endpoint.user.service import get_current_user


router = APIRouter(prefix="/article")


@router.post(
    "/{board_id}",
    response_model=ArticleGet,
    status_code=status.HTTP_201_CREATED,
    tags=["Article"],
)
async def create_article(
    board_id: int, _article_create: ArticleCreate, user=Depends(get_current_user)
) -> ArticleGet:
    """
    장작을 생성하는 라우팅 경로를 정의합니다.
    """
    return await service.create_article(
        name=_article_create.name,
        content=_article_create.content,
        board_id=board_id,
        user_id=user.id,
    )


@router.post(
    "/{board_id}/{prev_article_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Article"],
)
async def append_article(
    board_id: int,
    prev_article_id: int,
    _article_append: ArticleAppend,
    user=Depends(get_current_user),
) -> None:
    """
    불판에 장작을 추가할때 사용하는 라우팅 경로를 정의합니다.
    """
    await service.append_article(
        board_id=board_id,
        prev_article_id=prev_article_id,
        name=_article_append.name,
        content=_article_append.content,
        logic=_article_append.logic,
        user_id=user.id,
    )


@router.get("/{article_id}", response_model=ArticleGet, tags=["Article"])
async def get_article(article_id: int) -> ArticleGet:
    """
    장작을 조회하는 라우팅 경로를 정의합니다.
    """
    return await service.get_article_by_id(article_id)


@router.get("/list/{board_id}", response_model=list[ArticleGet], tags=["Article"])
async def get_article_list(board_id: int) -> list[ArticleGet]:
    """
    불판에 있는 모든 장작을 조회하는 경로를 정의합니다.
    """
    return await service.get_article_list_by_board_id(board_id)


# @router.get("/{article_id}/comment", response_model=list[CommentGet])

# @router.get("/{article_id}/like", response_model=ArticleLike)


@router.put("/{article_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Article"])
async def update_article(
    article_id: int, _article_update: ArticleUpdate, user=Depends(get_current_user)
) -> None:
    """
    장작을 수정하는 라우팅 경로를 정의합니다.
    """
    await service.update_article(
        article_id=article_id,
        name=_article_update.name,
        content=_article_update.content,
        user_id=user.id,
    )


@router.delete(
    "/{article_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Article"]
)
async def delete_article(article_id: int, user=Depends(get_current_user)) -> None:
    """
    장작을 삭제하는 라우팅 경로를 정의합니다.
    """
    await service.delete_article(article_id, user.id)
