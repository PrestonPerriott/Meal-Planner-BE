from typing import List
from ..data.model.grocery import GroceryItem
from ..data.model.meal_plan import MealPlan
from app.services.llm.local_llm import OllamsService
from app.services.llm.prompts.meal_planning import MealPlanningPrompts
from sqlmodel.ext.asyncio.session import AsyncSession

class MealPlannerService:
    def __init__(self, llm_service: OllamsService, db: AsyncSession):
        self.llm_service = llm_service
        self.db = db
        
    async def generate_meal_plans(self, selected_items: List[GroceryItem], num_meals: int = 3, max_time: int = 30, cuisine: str = "") -> str:
        """
        Generate a meal plan based on the selected items and the number of meals and max time.
        
        Args:
            selected_items: A list of GroceryItem objects representing the items the user has selected.
            num_meals: The number of meals to generate.
            max_time: The maximum time in minutes for each meal.
        """
        prompt = MealPlanningPrompts.construct_meal_prompt(selected_items, num_meals, max_time, cuisine)
        print(f"Prompt: {prompt}")
        response = await self.llm_service.generate_response(prompt)
        return response
    
    async def get_meal_plan(self, user_id: str, meal_plan_id: str | None = None, name: str | None = None) -> List[MealPlan]:
        """
        Get a meal plan for a user based on the meal plan id or name.
        """
        if meal_plan_id:
            query = query.where(MealPlan.id == meal_plan_id)
        elif name:
            query = query.where(MealPlan.name == name)
        return await self.db.exec(query).all()
    
    async def create_meal_plan(self, user_id: str, meal_plan: MealPlan) -> MealPlan:
        """
        Create a meal plan for a user.
        """
        pass
    
    async def update_meal_plan(self, user_id: str, meal_plan_id: str, meal_plan: MealPlan) -> MealPlan:
        """
        Update a meal plan for a user.
        """
        pass
    
    async def delete_meal_plan(self, user_id: str, meal_plan_id: str) -> None:
        """
        Delete a meal plan for a user.
        """
        pass