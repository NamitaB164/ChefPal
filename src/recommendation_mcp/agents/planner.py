
import json

import ollama
from pydantic import BaseModel, Field


class MealRequest(BaseModel):
    query: str = Field(min_length=1)
    max_calories: float | None = Field(default=None, ge=0)
    max_minutes: int | None = Field(default=None, ge=0)
    required_tags: list[str] = Field(default_factory=list)
    dietary_preferences: list[str] = Field(default_factory=list)


SYSTEM_PROMPT = """
You are a meal recommendation query planner.

Convert the user's request into a JSON object containing:
- main_food
- meal_type
- calories_limit
- preparation_time_limit
- dietary_preference

Rules:

1. MAIN FOOD
- Extract the food explicitly mentioned by the user.
- NEVER invent a food that the user did not mention.
- If no specific food is mentioned, set main_food to null.

2. MEAL TYPE
- Extract an explicitly stated meal type such as breakfast, lunch, or dinner.
- You may also preserve explicit food-type concepts such as salad or soup.
- NEVER invent a meal type that the user did not state.
- If no meal type is stated, set meal_type to null.

3. CALORIE LIMIT
- Extract only an explicitly stated numeric calorie limit.
- If there is no explicit numeric calorie limit, use null.
- NEVER estimate or invent a calorie limit.

4. PREPARATION TIME LIMIT
- Extract only an explicitly stated numeric preparation-time limit.
- If there is no explicit numeric time limit, use null.
- Words such as "quick", "fast", "easy", or "simple" do NOT imply a numeric time limit.
- NEVER convert "quick", "fast", "easy", or "simple" into a number.

5. DIETARY PREFERENCE
- Extract only explicitly stated dietary preferences such as:
  vegetarian, vegan, high protein, low sodium.
- NEVER infer a dietary preference.
- NEVER invent a dietary requirement.

Examples:

User: "I want a quick chicken recipe"
JSON:
{
  "main_food": "chicken",
  "meal_type": null,
  "calories_limit": null,
  "preparation_time_limit": null,
  "dietary_preference": null
}

User: "Give me a vegetarian breakfast under 400 calories"
JSON:
{
  "main_food": null,
  "meal_type": "breakfast",
  "calories_limit": 400,
  "preparation_time_limit": null,
  "dietary_preference": "vegetarian"
}

User: "I want a high protein dinner"
JSON:
{
  "main_food": null,
  "meal_type": "dinner",
  "calories_limit": null,
  "preparation_time_limit": null,
  "dietary_preference": "high protein"
}

User: "I want chicken dinner under 500 calories and ready in 30 minutes"
JSON:
{
  "main_food": "chicken",
  "meal_type": "dinner",
  "calories_limit": 500,
  "preparation_time_limit": 30,
  "dietary_preference": null
}

Return only valid JSON.
"""

class PlannerAgent:
    def __init__(self, model: str = "qwen2.5:3b"):
        self.model = model

    def plan(self, query: str) -> MealRequest:
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": query,
                },
            ],
            format="json",
        )

        parsed = json.loads(response.message.content)
        dietary_preference = parsed.get("dietary_preference")
        if dietary_preference:
            dietary_preference = dietary_preference.lower().strip()

            if dietary_preference == "highprotein":
                dietary_preference = "high protein"

        return MealRequest(
            query=" ".join(
                part
                for part in [
                    parsed.get("main_food"),
                    parsed.get("meal_type"),
                ]
                if part
            ),
            max_calories=parsed.get("calories_limit"),
            max_minutes=parsed.get("preparation_time_limit"),
            required_tags=[],
            dietary_preferences=(
                [dietary_preference]
                if dietary_preference
                else []
            ),
        )