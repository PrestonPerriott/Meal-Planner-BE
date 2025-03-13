from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from .base import BaseModel
import uuid
class GroceryItemBase(BaseModel):
    name: str | None = Field(default=None)
    brand: str | None = Field(default=None)
    image: str | None = Field(default=None, max_length=512)
    link: str | None = Field(default=None, max_length=512)
    price: float | None = Field(default=None)
    uom: str | None = Field(default=None, max_length=50)
    chain: str | None = Field(default=None, max_length=100)
    store: str | None = Field(default=None, max_length=100)
    
class GroceryItem(GroceryItemBase, table=True):
    __tablename__ = "grocery_item" # Explicitly set the table name
    meal_plan_id: Optional[uuid.UUID] = Field(default=None, foreign_key="meal_plan.id")
    meal_plan: Optional["MealPlan"] = Relationship(back_populates="ingredients")

class CreateGroceryItem(GroceryItemBase):
    pass

class GroceryItems(SQLModel):
    data: list[GroceryItem]
    count: int

# Avoid circualr dependency by importing at the end of the file
from .meal_plan import MealPlan
