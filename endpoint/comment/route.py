from fastapi import APIRouter, Depends, status

from endpoint.comment.service import create_comment, read_comment, get_comments_from_article, update_comment
from endpoint.comment.entity import CommentCreate, CommentUpdate, CommentGet
from endpoint.user.service import get_current_user


router = APIRouter(
    prefix="/comment"
)


@router.post("/", response_model=CommentGet, status_code=status.HTTP_201_CREATED)
async def create_comment(_comment_create: CommentCreate, user=Depends(get_current_user)):
    return await create_comment(
        content=_comment_create.content,
        article_id=_comment_create.article_id,
        creator_id=user.id
    )


@router.get("/{comment_id}", response_model=CommentGet)
async def get_comment(comment_id: int) -> CommentGet:
    return await read_comment(comment_id)


@router.get("/article/{article_id}", response_model=list[CommentGet])
async def get_comments(article_id: int) -> list[CommentGet]:
    return await get_comments_from_article(article_id)


@router.put("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_comment(comment_id: int, _comment_update: CommentUpdate, user=Depends(get_current_user)):
    await update_comment(
        comment_id=comment_id,
        user_id=user.id,
        content=_comment_update.content,
    )


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: int, user=Depends(get_current_user)):
    await delete_comment(comment_id, user.id)