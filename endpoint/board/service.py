"""
불판과 관련된 작업을 수행할 때, 구체적인 동작을 정의합니다.
"""

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from endpoint.board.repository import (
    get_board,
    create_board,
    update_board,
    delete_board,
    get_boards,
)
from data.db.models import Board, User


async def get_board_by_id(board_id: int) -> Board:
    """
    불판을 id를 입력받아 조회할 때의 구체적인 동작을 정의합니다.
    """
    try:
        res: Board = await get_board(board_id)
        if not res:
            raise HTTPException(status_code=400, detail="존재하지 않는 게시판입니다.")
    except IntegrityError as e:
        code: int = e.orig.pgcode
        if code == 23503:
            raise HTTPException(status_code=400, detail="존재하지 않는 게시글입니다.") from e
        raise HTTPException(
            status_code=500, detail=f"Unknown DB Error: {e.orig}"
        ) from e
    return res


async def get_board_list(per_page: int, page: int) -> list[Board]:
    """
    불판의 목록을 불러올 때의 구체적인 동작을 정의합니다.
    """
    try:
        res: list[Board] = await get_boards(per_page, page)
    except IntegrityError as e:
        code: int = e.orig.pgcode
        if code == 23503:
            raise HTTPException(status_code=400, detail="존재하지 않는 게시글입니다.") from e
        raise HTTPException(
            status_code=500, detail=f"Unknown DB Error: {e.orig}"
        ) from e

    return res


async def create_new_board(
    board_name: str, board_description: str, user_id: int, user: User
) -> Board:
    """
    새 불판을 생성할 때의 구체적인 동작을 정의합니다.
    """
    try:
        res = await create_board(
            {
                "name": board_name,
                "description": board_description,
                "creator_id": user_id,
                "creator": user,
            }
        )

        return res

    except IntegrityError as e:
        code: int = e.orig.pgcode
        if code == 23503:
            raise HTTPException(status_code=400, detail="존재하지 않는 유저입니다.") from e
        raise HTTPException(
            status_code=500, detail=f"Unknown DB Error: {e.orig}"
        ) from e


async def update_existing_board(
    board_id: int, board_name: str, board_description: str, user_id: int
) -> None:
    """
    현재 존재하는 불판의 이름과 설명을 수정할 때의 구체적인 동작을 정의합니다.
    """
    original_board = await get_board(board_id)
    if not original_board.name:
        raise HTTPException(status_code=400, detail="존재하지 않는 게시판입니다.")
    if not original_board.creator_id == user_id:
        raise HTTPException(status_code=401, detail="권한이 없습니다.")

    await update_board(
        board_id=original_board.id,
        board_req={"name": board_name, "description": board_description},
    )


async def delete_existing_board(board_id: int, user_id: int) -> None:
    """
    현재 존재하는 불판을 삭제할 때의 구체적인 동작을 정의합니다.
    """
    original_board = await get_board(board_id)
    if not original_board:
        raise HTTPException(status_code=400, detail="존재하지 않는 게시판입니다.")

    if not original_board.creator_id == user_id:
        raise HTTPException(status_code=401, detail="권한이 없습니다.")

    await delete_board(board_id)
