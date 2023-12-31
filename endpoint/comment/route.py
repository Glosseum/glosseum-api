from fastapi import APIRouter, Depends, status

import endpoint.comment.service as service
from endpoint.comment.entity import CommentCreate, CommentUpdate, CommentGet
from endpoint.user.service import get_current_user


router = APIRouter(prefix="/comment")


@router.post(
    "/{article_id}", response_model=CommentGet, status_code=status.HTTP_201_CREATED
)
async def create_comment(
    _comment_create: CommentCreate, article_id: int, user=Depends(get_current_user)
):
    return await service.create_new_comment(
        content=_comment_create.content, article_id=article_id, user_id=user.id
    )


@router.get("/{comment_id}", response_model=CommentGet)
async def get_comment(comment_id: int) -> CommentGet:
    return await service.read_comment_by_id(comment_id)


@router.get("/article/{article_id}", response_model=list[CommentGet])
async def get_comments(article_id: int) -> list[CommentGet]:
    return await service.read_comments_by_article(article_id)


@router.put("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_comment(
    comment_id: int, _comment_update: CommentUpdate, user=Depends(get_current_user)
):
    await service.update_comment(
        comment_id=comment_id,
        user_id=user.id,
        content=_comment_update.content,
    )


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: int, user=Depends(get_current_user)):
    await service.delete_comment(comment_id, user.id)
