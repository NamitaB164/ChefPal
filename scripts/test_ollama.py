import ollama

from recommendation_mcp.agents.planner import MealRequest

SYSTEM_PROMPT = """
You are a meal recommendation query planner.

Convert the user's request into the provided MealRequest schema.

Rules:
- query must contain only the main food or meal concept.
- Extract explicit calorie limits into max_calories.
- Extract explicit preparation-time limits into max_minutes.
- Explicit numeric calorie limits must always be stored in max_calories,
  never as dietary_preferences.
- Explicit numeric preparation-time limits must always be stored in
  max_minutes, never as dietary_preferences.
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
- Words such as "quick", "fast", or "easy" do not imply a numeric max_minutes value.
- Only set max_minutes when the user explicitly provides a numeric time limit.
- Never infer, estimate, assume, or choose a numeric value for max_minutes or max_calories.
- If the user does not explicitly provide a numeric value, the corresponding field MUST be null.
- A numeric calorie limit such as "under 500 calories" must NOT also be
  converted into a dietary preference such as "low calorie".
"""


queries = [
    "I want a chicken dinner under 500 calories that takes less than 30 minutes.",
    "I want a vegetarian meal.",
    "Something quick under 400 calories.",
    "I want pasta.",
    "I want a high protein chicken dinner.",
]


for query in queries:
    response = ollama.chat(
        model="qwen2.5:3b",
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

    print(f"\nQuery: {query}")
    print(response.message.content)