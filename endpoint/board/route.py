from fastapi import APIRouter, Depends, status

from endpoint.board.service import (
    get_board_by_id,
    get_board_list,
    create_new_board,
    update_existing_board,
    delete_existing_board,
)
from endpoint.board.entity import BoardGet, BoardCreate, BoardUpdate
from endpoint.user.service import get_current_user


router = APIRouter(prefix="/board")


@router.post("/", response_model=BoardGet, status_code=status.HTTP_201_CREATED)
async def create_board(_board_create: BoardCreate, user=Depends(get_current_user)):
    return await create_new_board(
        board_name=_board_create.name,
        board_description=_board_create.description,
        user_id=user.id,
    )


@router.get("/{board_id}", response_model=BoardGet)
async def get_board(board_id: int) -> BoardGet:
    return await get_board_by_id(board_id)


@router.get("/", response_model=list[BoardGet])
async def get_boards(per_page: int = 10, page: int = 1) -> list[BoardGet]:
    return await get_board_list(per_page, page)


@router.put("/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_board(
    board_id: int, _board_update: BoardUpdate, user=Depends(get_current_user)
):
    await update_existing_board(
        board_id=board_id,
        board_name=_board_update.name,
        board_description=_board_update.description,
        user_id=user.id,
    )


@router.delete("/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_board(board_id: int, user=Depends(get_current_user)):
    await delete_existing_board(board_id, user.id)
