import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio
async def test_get_board(test_client: AsyncClient):
    response = await test_client.get("/board/?per_page=10&page=1")

    assert response.status_code == status.HTTP_200_OK
