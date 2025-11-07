from __future__ import annotations

import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.anyio
async def test_liveness() -> None:
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}
