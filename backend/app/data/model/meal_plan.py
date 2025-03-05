from sqlmodel import Field, SQLModel
import uuid
import datetime
from typing import List, Optional
from .grocery import GroceryItem, get_utc_now

class MealPlanBase(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str | None = Field(default=None)
    ingredients: List[GroceryItem] = Field(default=[])
    suggested_meals: str = Field(default=None)
    created_at: datetime.datetime | None = Field(default_factory=get_utc_now)
    description: Optional[str] = None
    
class MealPlan(MealPlanBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    
class CreateMealPlan(MealPlanBase):
    pass

class MealPlans(SQLModel):
    data: list[MealPlan]
    count: int
    