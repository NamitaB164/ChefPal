
import json

import ollama
from pydantic import BaseModel, Field


class MealRequest(BaseModel):
    query: str = Field(min_length=1)
    max_calories: float | None = Field(default=None, ge=0)
    max_minutes: int | None = Field(default=None, ge=0)
    min_rating: float | None = Field(default=None, ge=0, le=5)
    required_tags: list[str] = Field(default_factory=list)
    dietary_preferences: list[str] = Field(default_factory=list)


SYSTEM_PROMPT = """
You are a meal recommendation query planner.

Convert the user's request into a JSON object containing exactly:
- main_food
- meal_type
- calories_limit
- preparation_time_limit
- min_rating
- dietary_preferences

Return dietary_preferences as a JSON array.

Rules:

1. MAIN FOOD
- Extract the specific food explicitly mentioned by the user.
- NEVER invent a food that the user did not mention.
- If no specific food is mentioned, set main_food to null.

2. MEAL TYPE
- Extract an explicitly stated meal type such as breakfast, lunch, or dinner.
- You may also preserve an explicitly stated food-type concept such as salad or soup.
- NEVER invent a meal type.
- If none is stated, set meal_type to null.

3. CALORIE LIMIT
- Extract only an explicitly stated numeric maximum calorie limit.
- "under 500 calories" means 500.
- "below 500 calories" means 500.
- "no more than 500 calories" means 500.
- If no numeric calorie limit is explicitly stated, use null.
- NEVER estimate or invent a calorie limit.

4. PREPARATION TIME LIMIT
- Extract only an explicitly stated numeric maximum preparation-time limit.
- "under 30 minutes" means 30.
- "no more than 30 minutes" means 30.
- "within 30 minutes" means 30.
- "30 minutes or less" means 30.
- Words such as "quick", "fast", "easy", or "simple" do NOT imply a numeric time limit.
- NEVER convert "quick", "fast", "easy", or "simple" into a number.
- If no numeric time limit is explicitly stated, use null.

5. MINIMUM RATING
- Extract only an explicitly stated numeric minimum rating.
- "rating above 4.0" means 4.0.
- "rating over 4.0" means 4.0.
- "rating of at least 4.0" means 4.0.
- "rated 4.0 or higher" means 4.0.
- If no numeric minimum rating is explicitly stated, use null.
- NEVER infer or invent a rating requirement.
- Words such as "good rating", "well rated", or "highly rated" do NOT imply a numeric rating.

6. DIETARY PREFERENCES
- Extract each explicitly stated dietary preference as a separate item.
- Examples include:
  vegetarian
  vegan
  high protein
  low sodium
  low calorie
  gluten free
  dairy free
- NEVER combine multiple preferences into one string.
- NEVER infer a dietary preference.
- NEVER invent a dietary requirement.
- If no dietary preference is explicitly stated, return [].

7. SOFT LANGUAGE
- Words such as "quick", "easy", "preferably", "ideally", "suitable", and "weeknight" are NOT dietary preferences.
- Do not put them in dietary_preferences.
- Do not convert them into numeric constraints unless the user explicitly provides a number.

Examples:

User: "I want a quick chicken recipe"

JSON:
{
  "main_food": "chicken",
  "meal_type": null,
  "calories_limit": null,
  "preparation_time_limit": null,
  "min_rating": null,
  "dietary_preferences": []
}

User: "Give me a vegetarian breakfast under 400 calories"

JSON:
{
  "main_food": null,
  "meal_type": "breakfast",
  "calories_limit": 400,
  "preparation_time_limit": null,
  "min_rating": null,
  "dietary_preferences": ["vegetarian"]
}

User: "I want a high protein dinner"

JSON:
{
  "main_food": null,
  "meal_type": "dinner",
  "calories_limit": null,
  "preparation_time_limit": null,
  "min_rating": null,
  "dietary_preferences": ["high protein"]
}

User: "I want chicken dinner under 500 calories and ready in 30 minutes"

JSON:
{
  "main_food": "chicken",
  "meal_type": "dinner",
  "calories_limit": 500,
  "preparation_time_limit": 30,
  "min_rating": null,
  "dietary_preferences": []
}

User: "I want a vegetarian high protein low sodium dinner"

JSON:
{
  "main_food": null,
  "meal_type": "dinner",
  "calories_limit": null,
  "preparation_time_limit": null,
  "min_rating": null,
  "dietary_preferences": ["vegetarian", "high protein", "low sodium"]
}

User: "Give me dinner recipes under 500 calories with a rating above 4.0"

JSON:
{
  "main_food": null,
  "meal_type": "dinner",
  "calories_limit": 500,
  "preparation_time_limit": null,
  "min_rating": 4.0,
  "dietary_preferences": []
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

        dietary_preferences = parsed.get("dietary_preferences", [])

        if isinstance(dietary_preferences, str):
            dietary_preferences = [dietary_preferences]

        dietary_preferences = [
            preference.lower().strip()
            for preference in dietary_preferences
            if preference
        ]

        dietary_preferences = [
            preference
            for preference in dietary_preferences
            if preference not in {
                "quick",
                "fast",
                "easy",
                "simple",
                "weeknight",
            }
        and "rating" not in preference
        ]

        dietary_preferences = [
            "high protein"
            if preference == "highprotein"
            else preference
            for preference in dietary_preferences
        ]
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
        min_rating=parsed.get("min_rating"),
        required_tags=[],
        dietary_preferences=dietary_preferences,
        )