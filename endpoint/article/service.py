"""
장작과 관련된 작업을 수행할 때, 구체적인 동작을 정의합니다.
"""

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

import endpoint.article.repository as repo
from endpoint.board.repository import get_board
from data.db.models import Article


async def create_article(
    name: str, content: str, board_id: int, user_id: int
) -> Article:
    """
    장작을 생성할 때의 구체적인 동작을 정의합니다.
    """
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
            raise HTTPException(status_code=400, detail="존재하지 않는 유저입니다.") from e
        raise HTTPException(
            status_code=500, detail=f"Unknown DB Error: {e.orig}"
        ) from e


async def append_article(
    prev_article_id: int,
    name: str,
    content: str,
    logic: str,
    board_id: int,
    user_id: int,
) -> None:
    """
    장작을 불판에 추가할 때의 구체적인 동작을 정의합니다.
    """
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
            raise HTTPException(status_code=400, detail="존재하지 않는 유저입니다.") from e
        raise HTTPException(
            status_code=500, detail=f"Unknown DB Error: {e.orig}"
        ) from e


async def get_article_by_id(article_id: int) -> Article:
    """
    장작의 id로 장작을 불러올 때의 구체적인 동작을 정의합니다.
    """
    try:
        res: Article = await repo.get_article(article_id)
        if not res:
            raise HTTPException(status_code=400, detail="존재하지 않는 게시글입니다.")
    except IntegrityError as e:
        code: int = e.orig.pgcode
        if code == 23503:
            raise HTTPException(status_code=400, detail="존재하지 않는 게시글입니다.") from e
        raise HTTPException(
            status_code=500, detail=f"Unknown DB Error: {e.orig}"
        ) from e
    return res


async def get_article_list_by_board_id(board_id: int) -> list[Article]:
    """
    불판의 id를 받아 장작의 목록을 불러올 때의 구체적인 동작을 정의합니다.
    """
    board = await get_board(board_id)
    if not board:
        raise HTTPException(status_code=400, detail="존재하지 않는 게시판입니다.")

    try:
        res: list[Article] = await repo.get_articles_from_board(board_id)
    except IntegrityError as e:
        code: int = e.orig.pgcode
        if code == 23503:
            raise HTTPException(status_code=400, detail="존재하지 않는 게시글입니다.") from e
        raise HTTPException(
            status_code=500, detail=f"Unknown DB Error: {e.orig}"
        ) from e

    return res


async def update_article(article_id: int, name: str, content: str, user_id: int):
    """
    장작을 수정할 때의 구체적인 동작을 정의합니다.
    """
    original_article: Article = await repo.get_article(article_id)

    if not original_article.name:
        raise HTTPException(status_code=400, detail="존재하지 않는 게시글입니다.")
    if not original_article.creator_id == user_id:
        raise HTTPException(status_code=401, detail="권한이 없습니다.")

    await repo.update_article(
        article_id=original_article.id, article_req={"name": name, "content": content}
    )


async def delete_article(article_id: int, user_id: int):
    """
    장작을 삭제할 때의 구체적인 동작을 정의합니다.
    """
    original_article: Article = await repo.get_article(article_id)

    if not original_article:
        raise HTTPException(status_code=400, detail="존재하지 않는 게시글입니다.")
    if not original_article.creator_id == user_id:
        raise HTTPException(status_code=401, detail="권한이 없습니다.")

    await repo.delete_article(article_id)
