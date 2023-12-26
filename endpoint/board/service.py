from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from endpoint.board.repository import get_board, create_board, update_board, delete_board, get_boards
from data.db.models import Board


async def get_board_by_id(board_id: int) -> Board:
    try:
        res: Board = await get_board(board_id)
    except IntegrityError as e:
        code: int = e.orig.pgcode
        if code == 23503:
            raise HTTPException(status_code=400, detail="존재하지 않는 게시글입니다.")
        else:
            raise HTTPException(status_code=500, detail=f"Unknown DB Error: {e.orig}")
    return res


async def get_board_list(per_page: int, page: int) -> list[Board]:
    try:
        res: list[Board] = await get_boards(per_page, page)
    except IntegrityError as e:
        code: int = e.orig.pgcode
        if code == 23503:
            raise HTTPException(status_code=400, detail="존재하지 않는 게시글입니다.")
        else:
            raise HTTPException(status_code=500, detail=f"Unknown DB Error: {e.orig}")

    return res


async def create_new_board(board_name: str, board_description: str, user_id: int) -> None:
    try:
        await create_board(
            {
                "creator_id": user_id,
                "name": board_name,
                "description": board_description
            }
        )
    except IntegrityError as e:
        code: int = e.orig.pgcode
        if code == 23503:
            raise HTTPException(status_code=400, detail="존재하지 않는 유저입니다.")
        else:
            raise HTTPException(status_code=500, detail=f"Unknown DB Error: {e.orig}")


async def update_existing_board(board_id: int, board_name: str, board_description: str, user_id: int):
    original_board = await get_board(board_id)
    if not original_board.name:
        raise HTTPException(status_code=400, detail="존재하지 않는 게시판입니다.")
    elif not original_board.creator_id == user_id:
        raise HTTPException(status_code=401, detail="권한이 없습니다.")

    await update_board(
        board_id=original_board.id,
        board_req={
            "name": board_name,
            "description": board_description
        }
    )


async def delete_existing_board(board_id: int, user_id: int):
    original_board = await get_board(board_id)
    if not original_board.creator_id == user_id:
        raise HTTPException(status_code=401, detail="권한이 없습니다.")

    await delete_board(board_id)
