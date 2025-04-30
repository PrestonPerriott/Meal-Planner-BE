from typing import List
from ....data.model.grocery import GroceryItem

class MealPlanningPrompts:
    @staticmethod
    def construct_meal_prompt(grocery_items: List[GroceryItem], num_meals: int, max_time: int, cuisine: str) -> str:
        items_text = "\n".join([f"- {item.name}" for item in grocery_items])

        return f"""Given these grocery items:
{items_text}

Please suggest {num_meals} easy-to-make meals that:
1. Use only these ingredients (or common household items like salt, pepper, oil, etc.)
2. Take {max_time} minutes or less to prepare
3. Are cost-effective
4. Include basic preparation instructions
5. Are simple for a beginner to make
6. Are {cuisine} cuisine
For each meal, please include:
- Name of the dish
- Estimated preparation time
- Estimated cost per serving
- Basic cooking instructions

Your response should only include the meals, no other text. You should assume the role of a personal chef.
"""