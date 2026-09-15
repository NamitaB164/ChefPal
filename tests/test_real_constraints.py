import asyncio

from recommendation_mcp.graph.workflow import build_graph


QUERIES = [
    {
        "query": "I want a chicken dinner under 500 calories and ready in 30 minutes",
        "max_calories": 500,
        "max_minutes": 30,
    },
    {
        "query": "Give me a vegetarian breakfast under 400 calories",
        "max_calories": 400,
        "max_minutes": None,
    },
]


async def main():
    graph = build_graph()

    for test_case in QUERIES:
        query = test_case["query"]

        print("\n" + "=" * 70)
        print(f"QUERY: {query}")
        print("=" * 70)

        result = await graph.ainvoke(
            {
                "user_query": query,
                "meal_request": None,
                "retrieval_result": None,
                "ranking_result": None,
            }
        )

        request = result["meal_request"]
        recommendations = result["ranking_result"].recommendations

        print("\nPlanner constraints:")
        print(f"max_calories = {request.max_calories}")
        print(f"max_minutes = {request.max_minutes}")
        print(f"dietary_preferences = {request.dietary_preferences}")

        print("\nConstraint validation:")

        for recommendation in recommendations:
            recipe = next(
                candidate.recipe
                for candidate in result["retrieval_result"].candidates
                if candidate.recipe_id == recommendation.recipe_id
            )

            calories_ok = (
                request.max_calories is None
                or recipe["calories_kcal"] <= request.max_calories
            )

            minutes_ok = (
                request.max_minutes is None
                or recipe["minutes"] <= request.max_minutes
            )

            print(
                f"{recommendation.recipe_id}: "
                f"{recipe['calories_kcal']:.1f} kcal, "
                f"{recipe['minutes']} min | "
                f"calories={'PASS' if calories_ok else 'FAIL'}, "
                f"time={'PASS' if minutes_ok else 'FAIL'}"
            )


if __name__ == "__main__":
    asyncio.run(main())