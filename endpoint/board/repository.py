"""
불판과 관련하여 데이터베이스와 실질적으로 상호작용하는 모듈입니다.
불판 : Board, 장작 : Article
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, insert
from data.db.database import Transactional
from data.db.models import Board


@Transactional()
async def get_board(board_id: int, session: AsyncSession = None) -> Board:
    """
    board_id를 바탕으로 불판을 데이터베이스에서 가져와 반환합니다.
    """
    stmt = select(Board).where(Board.id == board_id)

    res = await session.execute(stmt)

    return res.scalars().first()


@Transactional()
async def get_board_by_name(board_name: str, session: AsyncSession = None) -> Board:
    """
    board_name을 바탕으로 불판을 데이터베이스에서 가져와 반환합니다.
    """
    stmt = select(Board).where(Board.name == board_name)

    res = await session.execute(stmt)

    return res.scalars().first()


@Transactional()
async def get_boards(
    per_page: int, page: int, session: AsyncSession = None
) -> list[Board]:
    """
    불판을 데이터베이스에서 가져와 리스트 형태로 반환합니다.
    이때 id를 내림차 순으로 정렬합니다.
    """
    stmt = (
        select(Board)
        .limit(per_page)
        .order_by(Board.id.desc())
        .offset(per_page * (page - 1))
    )
    result = await session.execute(stmt)

    return result.scalars().all()


@Transactional()
async def create_board(board_req: dict, session: AsyncSession = None) -> Board:
    """
    불판을 생성한 후, 그 불판을 반환합니다.
    """
    _board = Board(**board_req)

    stmt = insert(Board)

    res = await session.execute(stmt)

    await session.commit()
    await session.refresh(_board)

    return res


@Transactional()
async def update_board(
    board_id: int, board_req: dict, session: AsyncSession = None
) -> None:
    """
    불판을 수정합니다.
    """
    stmt = update(Board).where(Board.id == board_id).values(**board_req)
    await session.execute(stmt)


@Transactional()
async def delete_board(board_id: int, session: AsyncSession = None) -> None:
    """
    불판을 삭제합니다.
    """
    stmt = delete(Board).where(Board.id == board_id)
    await session.execute(stmt)
