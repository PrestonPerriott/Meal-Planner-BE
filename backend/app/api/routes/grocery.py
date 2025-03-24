from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from ...data.model.grocery import GroceryItem
from app.core.db import get_db

router = APIRouter(prefix="/grocery", tags=["grocery"])

@router.get("/", response_model=List[GroceryItem])
# TODO: Add pagination
async def get_grocery_items(db: AsyncSession = Depends(get_db)):
    res = db.exec(select(GroceryItem))
    return res.all()

@router.get("/id/{item_id}", response_model=GroceryItem)
async def get_grocery_item(item_id: UUID, db: AsyncSession = Depends(get_db)):
    result = db.exec(select(GroceryItem).where(GroceryItem.id == item_id))
    item = result.first()
    if not item:
        raise HTTPException(status_code=404, detail="ID: Grocery item not found")
    return item

@router.get("/brand/{brand_name}", response_model=List[GroceryItem])
async def get_grocery_items_by_brand(brand_name: str, db: AsyncSession = Depends(get_db)):
    print(f"Getting grocery items by brand: {brand_name}")
    result = db.exec(select(GroceryItem).where(GroceryItem.brand == brand_name))
    items = result.all()
    if not items:
        raise HTTPException(status_code=404, detail="Brand: Grocery items not found")
    return items

@router.get("/name/{item_name}", response_model=List[GroceryItem])
async def get_grocery_items_by_item_name(item_name: str, db: AsyncSession = Depends(get_db)):
    result = db.exec(select(GroceryItem).where(GroceryItem.name == item_name))
    items = result.all()
    if not items:
        raise HTTPException(status_code=404, detail="Name: Grocery items not found")
    return items

@router.get("/type/{item_type}", response_model=List[GroceryItem])
async def get_grocery_items_by_item_type(item_type: str, db: AsyncSession = Depends(get_db)):
    result = db.exec(select(GroceryItem).where(GroceryItem.type == item_type))
    items = result.all()
    if not items:
        raise HTTPException(status_code=404, detail="Type: Grocery items not found")
    return items