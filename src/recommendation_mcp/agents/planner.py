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

Convert the user's request into the provided MealRequest schema.

Rules:
- query must contain the main food or meal concept.
- Preserve all meaningful food and meal terms from the user's request.
- Do not remove meaningful words such as "dinner", "breakfast", "lunch",
  "salad", "soup", or other meal-type terms.
- Do not reduce a multi-word food or meal concept to a single word.
- For example, "chicken dinner" must remain "chicken dinner".
- Extract explicit calorie limits into max_calories.
- Extract explicit preparation-time limits into max_minutes.
- Explicit numeric calorie limits must always be stored in max_calories,
  never as dietary_preferences.
- Explicit numeric preparation-time limits must always be stored in max_minutes,
  never as dietary_preferences.
- Never infer, estimate, assume, or choose a numeric value for max_minutes
  or max_calories.
- If the user does not explicitly provide a numeric value, the corresponding
  field MUST be null.
- Words such as "quick", "fast", or "easy" do not imply a numeric max_minutes value.
- Put qualitative dietary requirements such as vegetarian or vegan into
  dietary_preferences.
- dietary_preferences are only for qualitative preferences explicitly
  stated by the user, such as vegetarian, vegan, high protein, or low sodium.
- Do not convert numeric constraints into qualitative dietary_preferences.
- Do not invent constraints.
- Do not invent dataset tags.
- Leave optional fields null or empty when the user did not specify them.
- Never use "standard" or any other default dietary preference.
- dietary_preferences must contain only preferences explicitly stated by the user.
- Preserve the meaning of the user's request.
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
            format=MealRequest.model_json_schema(),
        )

        return MealRequest.model_validate_json(response.message.content)