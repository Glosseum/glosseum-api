"""
장작과 관련하여 데이터베이스와 실질적으로 상호작용하는 모듈입니다.
불판 : Board, 장작 : Article
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, insert
from data.db.database import Transactional
from data.db.models import Article


@Transactional()
async def get_article(article_id: int, session: AsyncSession = None) -> Article:
    """
    article_id를 바탕으로 장작을 데이터베이스에서 가져와서 반환합니다.
    """

    stmt = select(Article).where(Article.id == article_id)

    res = await session.execute(stmt)

    return res.scalars().first()


@Transactional()
async def get_articles_from_board(
    board_id: int, session: AsyncSession = None
) -> list[Article]:
    """
    불판에 있는 모든 장작을 조회하여 반환합니다.
    """

    stmt = (
        select(Article)
        .where(Article.board_id == board_id)
        .order_by(Article.path.desc())
    )
    result = await session.execute(stmt)

    return result.scalars().all()


@Transactional()
async def create_article(article_req: dict, session: AsyncSession = None) -> Article:
    """
    장작을 생성한 후, 그 장작을 반환합니다.
    """

    _article = Article(**article_req)

    session.add(_article)

    await session.commit()

    _article.path = _article.path + f"/{_article.id}"
    await session.commit()  # TODO: 2번 커밋보다 더 깔끔한 해결책을 찾자!

    await session.refresh(_article)

    return _article


@Transactional()
async def update_article(
    article_id: int, article_req: dict, session: AsyncSession = None
) -> None:
    """
    장작을 수정합니다.
    """

    stmt = update(Article).where(Article.id == article_id).values(**article_req)
    await session.execute(stmt)


@Transactional()
async def delete_article(article_id: int, session: AsyncSession = None) -> None:
    """
    장작을 삭제합니다.
    """
    stmt = delete(Article).where(Article.id == article_id)
    await session.execute(stmt)


@Transactional()
async def update_article_path(
    article_id: int, path: str, session: AsyncSession = None
) -> None:
    """
    장작의 경로를 수정합니다.
    """
    stmt = update(Article).where(Article.id == article_id).values(path=path)
    await session.execute(stmt)
