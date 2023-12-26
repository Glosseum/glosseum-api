from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from data.db.database import Transactional
from data.db.models import Board, User


@Transactional()
async def get_board(board_id: int, session: AsyncSession = None) -> Board:
    stmt = (
        select(Board)
        .where(Board.id == board_id)
    )

    res = await session.execute(stmt)

    return res.scalars().first()


@Transactional()
async def get_board_by_name(board_name: str, session: AsyncSession = None) -> Board:
    stmt = (
        select(Board)
        .where(Board.name == board_name)
    )

    res = await session.execute(stmt)

    return res.scalars().first()


@Transactional()
async def get_boards(per_page: int, page: int, session: AsyncSession = None) -> list[Board]:
    stmt = (
        select(Board)
        .limit(per_page)
        .order_by(Board.id.desc())
        .offset(per_page*(page-1))
    )
    result = await session.execute(stmt)

    return result.scalars().all()


@Transactional()
async def create_board(board_req: dict, session: AsyncSession = None) -> None:
    _board = Board(**board_req)

    session.add(_board)

    await session.commit()
    await session.refresh(_board)


@Transactional()
async def update_board(board_id: int, board_req: dict, session: AsyncSession = None) -> None:
    stmt = (
        update(Board)
        .where(Board.id == board_id).values(**board_req)
    )
    await session.execute(stmt)


@Transactional()
async def delete_board(board_id: int, session: AsyncSession = None) -> None:
    stmt = delete(Board).where(Board.id == board_id)
    await session.execute(stmt)
