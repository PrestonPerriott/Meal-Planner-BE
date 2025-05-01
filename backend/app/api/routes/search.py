from fastapi import APIRouter, Query, Depends, HTTPException
from app.core.db import get_db

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/semantic")
async def semantic_search(
    query: str,
    limit: int = Query(10, ge=1, le=100)
):
    pass