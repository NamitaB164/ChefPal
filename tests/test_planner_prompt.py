import ollama

SYSTEM_PROMPT = """
You are a meal recommendation query planner.

Convert the user's request into a structured meal request.

Rules:
- query must contain the main food or meal concept.
- Preserve meaningful food and meal terms.
- Extract explicit calorie limits.
- Extract explicit preparation-time limits.
- Put qualitative dietary requirements such as vegetarian, vegan,
  or high protein into dietary preferences.
- Do not invent constraints.
"""

print("before")

response = ollama.chat(
    model="qwen2.5:3b",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                "I want a high protein chicken dinner under "
                "500 calories and ready in 30 minutes"
            ),
        },
    ],
    format="json",
)

print("after")
print(response.message.content)