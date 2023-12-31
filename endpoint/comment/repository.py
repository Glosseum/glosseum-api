from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from data.db.database import Transactional
from data.db.models import Board, User, Article, Comment


@Transactional()
async def create_comment(comment_req: dict, session: AsyncSession = None) -> Comment:
    _comment = Comment(**comment_req)

    session.add(_comment)

    await session.commit()
    await session.refresh(_comment)

    return _comment


@Transactional()
async def get_comment(comment_id: int, session: AsyncSession = None) -> Comment:
    stmt = select(Comment).where(Comment.id == comment_id)

    res = await session.execute(stmt)

    return res.scalars().first()


@Transactional()
async def get_comments_from_article(
    article_id: int, session: AsyncSession = None
) -> list[Comment]:
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
    stmt = update(Comment).where(Comment.id == comment_id).values(**comment_req)
    await session.execute(stmt)

    return await get_comment(comment_id)


@Transactional()
async def delete_comment(comment_id: int, session: AsyncSession = None) -> None:
    stmt = delete(Comment).where(Comment.id == comment_id)
    await session.execute(stmt)
