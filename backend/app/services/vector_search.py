from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models
from app.core.config import settings
from app.data.model.grocery import GroceryItem

class VectorSearchService:
    def __init__(self, collection_name: str):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = QdrantClient(url=settings.QDRANT_HOST)
        self.collection_name = collection_name
        self._ensure_collection_exists()
        
    def _ensure_collection_exists(self):
        collections = self.client.get_collections()
        collection_names = [collection.name for collection in collections]
        if self.collection_name not in collection_names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE)
            )
    
    def _create_embedding(self, text: str) -> List[float]:
        return self.model.encode(text).tolist()
    
    def _construct_grocery_text(self, item: GroceryItem) -> str:
        """Create a text representation of a grocery item for embedding"""
        parts = []
        if item.name:
            parts.append(item.name)
        if item.brand:
            parts.append(f"Brand: {item.brand}")
        if item.type:
            parts.append(f"Type: {item.type}")
        if item.chain:
            parts.append(f"Store: {item.chain}")
        return " ".join(parts)
    
    def index_grocery_item(self, item: GroceryItem):
        pass
    
    def index_grocery_items(self, items: List[GroceryItem]):
        points = []
        for item in items:
            text = self._construct_grocery_text(item)
            embedding = self._create_embedding(text)
            points.append(models.PointStruct(
                id=str(item.id),
                vector=embedding,
                payload={
                    "id": str(item.id),
                    "name": item.name,
                    "brand": item.brand,
                    "type": item.type,
                    "price": item.price,
                    "chain": item.chain,
                    "store": item.store,
                    "image_url": item.image,
                    "link": item.link,
                    "uom": item.uom
                }
            ))
        
        if points:
            self.client.upsert(collection_name=self.collection_name, points=points)
    
    def search_similar_items(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        embedded_query = self._create_embedding(query)
        
        result = self.client.search(
            collection_name=self.collection_name,
            query_vector=embedded_query,
            limit=limit
        )
        
        return [item.payload for item in result]
    
    