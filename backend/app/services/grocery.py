from typing import List
from ..data.model.grocery import GroceryItem, CreateGroceryItem, GroceryItems
from app.services.vector_search import VectorSearchService
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
import uuid

class GroceryService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.vector_search = VectorSearchService()
        
    async def create_grocery_item(self, item: CreateGroceryItem) -> GroceryItem:
        db_item = GroceryItem.model_validate(item)
        self.db.add(db_item)
        await self.db.commit()
        await self.db.refresh(db_item)
        
        # Index item for vector search
        await self.vector_search.index_grocery_item(db_item)
        return db_item
    
    async def get_grocery_item(self, item_id: uuid.UUID | None = None, name: str | None = None) -> GroceryItem | None:
        if item_id:
            return await self.db.get(GroceryItem, item_id)
        elif name:
            return await self.db.exec(select(GroceryItem).where(GroceryItem.name == name)).first()
        return None
    
    async def get_grocery_items(self, item_ids: List[uuid.UUID] | None = None, names: List[str] | None = None, brands: List[str] | None = None, types: List[str] | None = None) -> List[GroceryItem]:
        query = select(GroceryItem)
        if item_ids:
            query = query.where(GroceryItem.id.in_(item_ids))
        elif names:
            query = query.where(GroceryItem.name.in_(names))
        elif brands:
            query = query.where(GroceryItem.brand.in_(brands))
        elif types:
            query = query.where(GroceryItem.type.in_(types))
        return await self.db.exec(query).all()
    
    