from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

import endpoint.article.repository as repo
from endpoint.board.repository import get_board
from data.db.models import Board, User, Article


async def create_article(name: str, content: str, board_id: int, user_id: int) -> Article:
    prev: list = await repo.get_articles_from_board(board_id)
    if len(prev) != 0:
        raise HTTPException(status_code=400, detail="이미 게시글이 존재하는 게시판입니다, 게시글을 추가해주세요.")

    try:
        res = await repo.create_article(
            {
                "name": name,
                "content": content,
                "board_id": board_id,
                "creator_id": user_id,
                "path": "",
                "path_logical": "ROOT",
            }
        )
        return res
    except IntegrityError as e:
        code: int = e.orig.pgcode
        if code == 23503:
            raise HTTPException(status_code=400, detail="존재하지 않는 유저입니다.")
        else:
            raise HTTPException(status_code=500, detail=f"Unknown DB Error: {e.orig}")


async def append_article(
    prev_article_id: int,
    name: str,
    content: str,
    logic: str,
    board_id: int,
    user_id: int,
) -> None:
    prev_article: Article = await repo.get_article(prev_article_id)
    if not prev_article:
        raise HTTPException(status_code=400, detail="존재하지 않는 게시글입니다.")

    try:
        await repo.create_article(
            {
                "name": name,
                "content": content,
                "board_id": board_id,
                "creator_id": user_id,
                "path": prev_article.path,
                "path_logical": prev_article.path_logical + f"/{logic}",
            }
        )
    except IntegrityError as e:
        code: int = e.orig.pgcode
        if code == 23503:
            raise HTTPException(status_code=400, detail="존재하지 않는 유저입니다.")
        else:
            raise HTTPException(status_code=500, detail=f"Unknown DB Error: {e.orig}")


async def get_article_by_id(article_id: int) -> Article:
    try:
        res: Article = await repo.get_article(article_id)
        if not res:
            raise HTTPException(status_code=400, detail="존재하지 않는 게시글입니다.")
    except IntegrityError as e:
        code: int = e.orig.pgcode
        if code == 23503:
            raise HTTPException(status_code=400, detail="존재하지 않는 게시글입니다.")
        else:
            raise HTTPException(status_code=500, detail=f"Unknown DB Error: {e.orig}")
    return res


async def get_article_list_by_board_id(board_id: int) -> list[Article]:
    board = await get_board(board_id)
    if not board:
        raise HTTPException(status_code=400, detail="존재하지 않는 게시판입니다.")

    try:
        res: list[Article] = await repo.get_articles_from_board(board_id)
    except IntegrityError as e:
        code: int = e.orig.pgcode
        if code == 23503:
            raise HTTPException(status_code=400, detail="존재하지 않는 게시글입니다.")
        else:
            raise HTTPException(status_code=500, detail=f"Unknown DB Error: {e.orig}")

    return res


async def update_article(article_id: int, name: str, content: str, user_id: int):
    original_article: Article = await repo.get_article(article_id)

    if not original_article.name:
        raise HTTPException(status_code=400, detail="존재하지 않는 게시글입니다.")
    elif not original_article.creator_id == user_id:
        raise HTTPException(status_code=401, detail="권한이 없습니다.")

    await repo.update_article(
        article_id=original_article.id, article_req={"name": name, "content": content}
    )


async def delete_article(article_id: int, user_id: int):
    original_article: Article = await repo.get_article(article_id)

    if not original_article:
        raise HTTPException(status_code=400, detail="존재하지 않는 게시글입니다.")
    elif not original_article.creator_id == user_id:
        raise HTTPException(status_code=401, detail="권한이 없습니다.")

    await repo.delete_article(article_id)
