import asyncio
from sqlmodel import select
from app.data.model.grocery import GroceryItem
from app.services.vector_search import VectorSearchService
from app.core.db import get_db_session
from tqdm import tqdm
from app.core.config import settings

async def index_vector_db():
    """Index all grocery items into the vector database"""
    if not settings.INDEX_VECTOR_DB:
        print("Vector database indexing is disabled")
        return
    
    db = get_db_session()
    vector_search = VectorSearchService(collection_name="grocery_items")
    
    try:
        grocery_items = db.exec(select(GroceryItem))
        all_groceries = grocery_items.all()
        
        print(f"Indexing {len(all_groceries)} grocery items...")
        batch_size = 100
        for i in tqdm(range(0, len(all_groceries), batch_size)):
            batch = all_groceries[i:i+batch_size]
            vector_search.index_grocery_items(batch)
            print(f"Indexed batch {i//batch_size + 1}/{(len(all_groceries)-1)//batch_size + 1}")
        
        print("Vector database indexing of grocery items complete")
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(index_vector_db())