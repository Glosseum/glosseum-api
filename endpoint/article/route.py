from fastapi import APIRouter, Depends, status

import endpoint.article.service as service
from endpoint.article.entity import (
    ArticleCreate,
    ArticleAppend,
    ArticleUpdate,
    ArticleGet,
)
from endpoint.user.service import get_current_user


router = APIRouter(prefix="/article")


@router.post("/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
async def create_article(
    board_id: int, _article_create: ArticleCreate, user=Depends(get_current_user)
) -> None:
    # TODO: 보드에 이미 게시글이 있으면 Create는 에러가 나야 함
    await service.create_article(
        name=_article_create.name,
        content=_article_create.content,
        board_id=board_id,
        user_id=user.id,
    )


@router.post("/{board_id}/{prev_article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def append_article(
    board_id: int,
    prev_article_id: int,
    _article_append: ArticleAppend,
    user=Depends(get_current_user),
) -> None:
    await service.append_article(
        board_id=board_id,
        prev_article_id=prev_article_id,
        name=_article_append.name,
        content=_article_append.content,
        logic=_article_append.logic,
        user_id=user.id,
    )


@router.get("/{article_id}", response_model=ArticleGet)
async def get_article(article_id: int) -> ArticleGet:
    return await service.get_article_by_id(article_id)


@router.get("/list/{board_id}", response_model=list[ArticleGet])
async def get_article_list(board_id: int) -> list[ArticleGet]:
    return await service.get_article_list_by_board_id(board_id)


# @router.get("/{article_id}/comment", response_model=list[CommentGet])

# @router.get("/{article_id}/like", response_model=ArticleLike)


@router.put("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_article(
    article_id: int, _article_update: ArticleUpdate, user=Depends(get_current_user)
) -> None:
    await service.update_article(
        article_id=article_id,
        name=_article_update.name,
        content=_article_update.content,
        user_id=user.id,
    )


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(article_id: int, user=Depends(get_current_user)) -> None:
    await service.delete_article(article_id, user.id)
