from typing import List
from ....data.model.grocery import GroceryItem

class MealPlanningPrompts:
    @staticmethod
    def generate_meal_suggestions(grocery_items: List[GroceryItem], num_meals: int, max_time: int) -> str:
        items_text = "\n".join([f"- {item.name} (${item.price:.2f}) per {item.uom})" for item in grocery_items])

        return f"""Given these grocery items:
{items_text}

Please suggest {num_meals} easy-to-make meals that:
1. Use only these ingredients (or common household items like salt, pepper, oil)
2. Take {max_time} minutes or less to prepare
3. Are cost-effective
4. Include basic preparation instructions

For each meal, please include:
- Name of the dish
- Estimated preparation time
- Estimated cost per serving
- Basic cooking instructions
"""