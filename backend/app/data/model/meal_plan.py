from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional
from .base import BaseModel

class MealPlanBase(BaseModel):
    name: str | None = Field(default=None)
    suggested_meals: str = Field(default=None)
    description: Optional[str] = None
    
class MealPlan(MealPlanBase, table=True):
    __tablename__ = "meal_plan" # Explicitly set the table name
    ingredients: List["GroceryItem"] = Relationship(back_populates="meal_plan")
    
class CreateMealPlan(MealPlanBase):
    pass

class MealPlans(SQLModel):
    data: list[MealPlan]
    count: int

# Avoid circualr dependency by importing at the end of the file
from .grocery import GroceryItem