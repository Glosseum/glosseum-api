from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, event
from data.db.database import Transactional
from data.db.models import Board, User, Article


@Transactional()
async def get_article(article_id: int, session: AsyncSession = None) -> Article:
    stmt = (
        select(Article)
        .where(Article.id == article_id)
    )

    res = await session.execute(stmt)

    return res.scalars().first()


@Transactional()
async def get_articles_from_board(board_id: int, session: AsyncSession = None) -> list[Article]:
    stmt = (
        select(Article)
        .where(Article.board_id == board_id)
        .order_by(Article.path.desc())
    )
    result = await session.execute(stmt)

    return result.scalars().all()


@Transactional()
async def create_article(article_req: dict, session: AsyncSession = None) -> None:
    _article = Article(**article_req)

    session.add(_article)

    await session.commit()

    _article.path = _article.path + f"/{_article.id}"
    await session.commit()

    await session.refresh(_article)

    print(_article.__dict__)


@Transactional()
async def update_article(article_id: int, article_req: dict, session: AsyncSession = None) -> None:
    stmt = (
        update(Article)
        .where(Article.id == article_id).values(**article_req)
    )
    await session.execute(stmt)


@Transactional()
async def delete_article(article_id: int, session: AsyncSession = None) -> None:
    stmt = delete(Article).where(Article.id == article_id)
    await session.execute(stmt)


@Transactional()
async def update_article_path(article_id: int, path: str, session: AsyncSession = None) -> None:
    stmt = (
        update(Article)
        .where(Article.id == article_id).values(path=path)
    )
    await session.execute(stmt)
