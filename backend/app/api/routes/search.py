from fastapi import APIRouter, Query, Depends, HTTPException, Body
from app.core.db import get_db
from app.services.vector_search import VectorSearchService
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID
router = APIRouter(prefix="/search", tags=["search"])
search_service = VectorSearchService(collection_name="grocery_items")

@router.post("/semantic/")
async def semantic_search(
    query: str = Body(..., embed=True),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Semantic search for items"""
    try:
        print(f"Semantic Search Route: Searching for {query} with limit {limit}")
        results = search_service.search_similar_items(query, limit)
        return {"results": results, "status": "success", "count": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search Error: {str(e)}")
    
@router.post("/similar/{item_id}")
async def similar_search(
    item_id: UUID,
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Search for similar items by ID"""
    try:
        results = await search_service.search_similar_by_id(item_id, limit)
        return {"results": results, "status": "success", "count": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Similar Search Error: {str(e)}")
