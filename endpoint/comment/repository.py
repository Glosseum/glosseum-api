"""
댓글과 관련하여 데이터베이스와 실질적으로 상호작용하는 모듈입니다.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from data.db.database import Transactional
from data.db.models import Comment


@Transactional()
async def create_comment(comment_req: dict, session: AsyncSession = None) -> Comment:
    """
    comment_req를 바탕으로 댓글을 생성한 후, 반환합니다.
    """
    _comment = Comment(**comment_req)

    session.add(_comment)

    await session.commit()
    await session.refresh(_comment)

    return _comment


@Transactional()
async def get_comment(comment_id: int, session: AsyncSession = None) -> Comment:
    """
    comment_id를 바탕으로 댓글을 데이터베이스에서 가져와 반환합니다.
    """
    stmt = select(Comment).where(Comment.id == comment_id)

    res = await session.execute(stmt)

    return res.scalars().first()


@Transactional()
async def get_comments_from_article(
    article_id: int, session: AsyncSession = None
) -> list[Comment]:
    """
    장작의 id를 바탕으로 장작에 달린 모든 댓글을 조회합니다.
    """
    stmt = (
        select(Comment)
        .where(Comment.article_id == article_id)
        .order_by(Comment.id.desc())
    )
    res = await session.execute(stmt)

    return res.scalars().all()


@Transactional()
async def update_comment(
    comment_id: int, comment_req: dict, session: AsyncSession = None
) -> None:
    """
    댓글의 id와 comment_req를 바탕으로 댓글을 수정합니다.
    """
    stmt = update(Comment).where(Comment.id == comment_id).values(**comment_req)
    await session.execute(stmt)

    return await get_comment(comment_id)


@Transactional()
async def delete_comment(comment_id: int, session: AsyncSession = None) -> None:
    """
    댓글의 id를 바탕으로 댓글을 삭제합니다.
    """
    stmt = delete(Comment).where(Comment.id == comment_id)
    await session.execute(stmt)
