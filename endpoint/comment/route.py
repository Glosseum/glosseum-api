"""
댓글과 관련된 모든 라우팅 경로 URL을 정의합니다.
"""

from fastapi import APIRouter, Depends, status

from endpoint.comment import service
from endpoint.comment.entity import CommentCreate, CommentUpdate, CommentGet
from endpoint.user.service import get_current_user


router = APIRouter(prefix="/comment")


@router.post(
    "/{article_id}",
    response_model=CommentGet,
    status_code=status.HTTP_201_CREATED,
    tags=["Comment"],
)
async def create_comment(
    _comment_create: CommentCreate, article_id: int, user=Depends(get_current_user)
):
    """
    댓글을 생성하는 라우팅 경로를 정의합니다.
    """
    return await service.create_new_comment(
        content=_comment_create.content, article_id=article_id, user_id=user.id
    )


@router.get("/{comment_id}", response_model=CommentGet, tags=["Comment"])
async def get_comment(comment_id: int) -> CommentGet:
    """
    특정 댓글을 조회하는 라우팅 경로를 정의합니다.
    """
    return await service.read_comment_by_id(comment_id)


@router.get("/article/{article_id}", response_model=list[CommentGet], tags=["Comment"])
async def get_comments(article_id: int) -> list[CommentGet]:
    """
    장작에 달려있는 댓글 목록을 조회하는 라우팅 경로를 정의합니다.
    """
    return await service.read_comments_by_article(article_id)


@router.put("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Comment"])
async def update_comment(
    comment_id: int, _comment_update: CommentUpdate, user=Depends(get_current_user)
):
    """
    댓글을 수정하는 라우팅 경로를 정의합니다.
    """
    await service.update_comment(
        comment_id=comment_id,
        user_id=user.id,
        content=_comment_update.content,
    )


@router.delete(
    "/{comment_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Comment"]
)
async def delete_comment(comment_id: int, user=Depends(get_current_user)):
    """
    댓글을 삭제하는 라우팅 경로를 정의합니다.
    """
    await service.delete_comment(comment_id, user.id)
