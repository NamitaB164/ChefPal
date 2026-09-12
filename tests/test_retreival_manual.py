import asyncio

from recommendation_mcp.agents.planner import MealRequest
from recommendation_mcp.agents.retrieval import RetrievalAgent
from recommendation_mcp.mcp_client.client import RecommendationMCPClient


async def main():
    client = RecommendationMCPClient()
    agent = RetrievalAgent(client)

    request = MealRequest(
        query="chicken dinner",
        max_calories=500,
        max_minutes=30,
    )

    result = await agent.retrieve(request)

    print(f"Candidates: {len(result.candidates)}")

    for candidate in result.candidates:
        print(
            candidate.recipe_id,
            candidate.score,
            candidate.recipe["name"],
            candidate.recipe["calories_kcal"],
            candidate.recipe["minutes"],
        )


if __name__ == "__main__":
    asyncio.run(main())