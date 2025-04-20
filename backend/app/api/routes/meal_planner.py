from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from ...services.meal_planner import MealPlannerService
from ...services.llm.local_llm import OllamsService
from ...data.model.meal_plan import MealPlan, CreateMealPlan, MealPlan, MealPlans
from ...data.model.grocery import GroceryItem
from app.core.db import get_db

router = APIRouter(prefix="/meal-planner", tags=["meal-planner"])
llm_service = OllamsService()

@router.post("/generate-meals", response_model=MealPlan)
async def generate_meals(
    selected_items: List[UUID],
    num_meals: int = 3,
    max_time: int = 30,
    cuisine: str = "Any",
    db: AsyncSession = Depends(get_db)
):
    meal_planner_service = MealPlannerService(llm_service, db)
    result = db.exec(select(GroceryItem).where(GroceryItem.id.in_(selected_items)))
    grocery_items = result.all()
    
    if not grocery_items:
        raise HTTPException(status_code=404, detail="Grocery items not found")
    
    meal_plans = await meal_planner_service.generate_meal_plans(grocery_items, num_meals, max_time, cuisine)
    return {"meal_suggestions": meal_plans}
    
    