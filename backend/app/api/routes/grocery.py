from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from ...data.model.grocery import GroceryItem
from backend.app.core.db import get_db

router = APIRouter(prefix="/grocery", tags=["grocery"])

@router.get("/", response_model=List[GroceryItem])
async def get_grocery_items(db: AsyncSession = Depends(get_db)):
    return await db.exec(select(GroceryItem)).all()

@router.get("/{item_id}", response_model=GroceryItem)
async def get_grocery_item(item_id: UUID, db: AsyncSession = Depends(get_db)):
    item = await db.exec(select(GroceryItem).where(GroceryItem.id == item_id)).first()
    if not item:
        raise HTTPException(status_code=404, detail="Grocery item not found")
    return item

@router.get("/{brand_name}", response_model=List[GroceryItem])
async def get_grocery_items_by_brand(brand_name: str, db: AsyncSession = Depends(get_db)):
    return await db.exec(select(GroceryItem).where(GroceryItem.brand_name == brand_name)).all()

@router.get("/{item_name}", response_model=List[GroceryItem])
async def get_grocery_items_by_item_name(item_name: str, db: AsyncSession = Depends(get_db)):
    return await db.exec(select(GroceryItem).where(GroceryItem.item_name == item_name)).all()
