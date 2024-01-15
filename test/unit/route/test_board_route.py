import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio
async def test_get_board(test_client: AsyncClient):
    response = await test_client.get("/board/?per_page=10&page=1")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_post_board(test_client: AsyncClient, test_headers: dict):
    response = await test_client.post(
        "/board/",
        json={
            "name": "test",
            "description": "test",
        },
        headers=test_headers,
    )

    print(response.content)

    assert response.status_code == status.HTTP_204_NO_CONTENT
