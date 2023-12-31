from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

import endpoint.comment.repository as repo
from data.db.models import Board, User, Article, Comment


async def create_new_comment(
    content: str, article_id: int, user_id: int
) -> Comment | None:
    if len(content) >= 100:
        raise HTTPException(status_code=400, detail="댓글은 100자 이내여야 합니다.")

    try:
        res = await repo.create_comment(
            {"content": content, "article_id": article_id, "creator_id": user_id}
        )
        return res
    except IntegrityError as e:
        code: int = e.orig.pgcode
        if code == 23503:
            raise HTTPException(status_code=400, detail="존재하지 않는 유저입니다.")
        else:
            raise HTTPException(status_code=500, detail=f"Unknown DB Error: {e.orig}")


async def read_comment_by_id(comment_id: int) -> Article:
    try:
        res: Article = await repo.get_comment(comment_id)
        if not res:
            raise HTTPException(status_code=400, detail="존재하지 않는 댓글입니다.")
    except IntegrityError as e:
        code: int = e.orig.pgcode
        if code == 23503:
            raise HTTPException(status_code=400, detail="존재하지 않는 게시글입니다.")
        else:
            raise HTTPException(status_code=500, detail=f"Unknown DB Error: {e.orig}")

    return res


async def read_comments_by_article(article_id: int) -> list[Article]:
    try:
        res: list[Article] = await repo.get_comments_from_article(article_id)
    except IntegrityError as e:
        code: int = e.orig.pgcode
        if code == 23503:
            raise HTTPException(status_code=400, detail="존재하지 않는 게시글입니다.")
        else:
            raise HTTPException(status_code=500, detail=f"Unknown DB Error: {e.orig}")

    return res


async def update_comment(comment_id: int, content: str, user_id: int) -> None:
    original_comment = await repo.get_comment(comment_id)
    if not original_comment:
        raise HTTPException(status_code=400, detail="존재하지 않는 댓글입니다.")
    elif not original_comment.creator_id == user_id:
        raise HTTPException(status_code=401, detail="권한이 없습니다.")

    await repo.update_comment(
        comment_id=original_comment.id, comment_req={"content": content}
    )


async def delete_comment(comment_id: int, user_id: int) -> None:
    original_comment = await repo.get_comment(comment_id)
    if not original_comment:
        raise HTTPException(status_code=400, detail="존재하지 않는 댓글입니다.")
    elif not original_comment.creator_id == user_id:
        raise HTTPException(status_code=401, detail="권한이 없습니다.")

    await repo.delete_comment(comment_id=original_comment.id)
