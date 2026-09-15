import asyncio

from recommendation_mcp.graph.workflow import build_graph


QUERIES = [
    "I want a chicken dinner under 500 calories and ready in 30 minutes",
    "Give me a vegetarian breakfast under 400 calories",
    "I want a quick chicken recipe",
    "Give me a high protein dinner",
]


async def main():
    graph = build_graph()

    for query in QUERIES:
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

        print("\nMeal request:")
        print(result["meal_request"])

        print("\nRecommendations:")
        for recommendation in result["ranking_result"].recommendations:
            print(recommendation)


if __name__ == "__main__":
    asyncio.run(main())