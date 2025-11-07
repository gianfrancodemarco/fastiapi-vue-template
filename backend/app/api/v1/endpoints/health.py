from __future__ import annotations

from fastapi import APIRouter


router = APIRouter()


@router.get("/live")
async def liveness() -> dict[str, str]:
    return {"status": "alive"}


@router.get("/ready")
async def readiness() -> dict[str, str]:
    return {"status": "ready"}
