from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from endpoint.board.repository import get_board, create_board, update_board, delete_board


async def get_board_by_id(board_id: int):
    try:
        board = await get_board(board_id)
    except IntegrityError as e:
        pass
