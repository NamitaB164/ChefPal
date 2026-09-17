import asyncio

from recommendation_mcp.graph.workflow import build_graph


QUERIES = [
    "I want a high-protein vegetarian dinner with chicken-style savory flavors, under 500 calories, that takes no more than 30 minutes to prepare. It should be low sodium, suitable for a quick weeknight meal, and preferably have a rating above 4.0. Please give me 5 different recipes, with the highest-protein options first.",
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