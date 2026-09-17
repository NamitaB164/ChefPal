import asyncio
import time

from recommendation_mcp.agents.planner import PlannerAgent
from recommendation_mcp.agents.retrieval import RetrievalAgent
from recommendation_mcp.agents.ranking import RankingAgent
from recommendation_mcp.mcp_client.client import RecommendationMCPClient


async def main():
    query = (
        "I want a high protein chicken dinner under "
        "500 calories and ready in 30 minutes"
    )

    print("=== PLANNER ===")
    start = time.perf_counter()

    planner = PlannerAgent()
    meal_request = planner.plan(query)

    print(f"Finished in {time.perf_counter() - start:.2f}s")
    print(meal_request)

    print("\n=== RETRIEVAL ===")
    start = time.perf_counter()

    client = RecommendationMCPClient()
    retrieval = RetrievalAgent(client)

    retrieval_result = await retrieval.retrieve(meal_request)

    print(f"Finished in {time.perf_counter() - start:.2f}s")
    print(f"Candidates: {len(retrieval_result.candidates)}")

    for candidate in retrieval_result.candidates:
        print(
            candidate.recipe_id,
            candidate.score,
            candidate.recipe["name"],
        )

    print("\n=== RANKING ===")
    start = time.perf_counter()

    ranking = RankingAgent()
    ranking_result = await ranking.rank(
        request=meal_request,
        candidates=retrieval_result.candidates,
    )

    print(f"Finished in {time.perf_counter() - start:.2f}s")

    for recommendation in ranking_result.recommendations:
        print(
            recommendation.recipe_id,
            recommendation.score,
            recommendation.reason,
        )


if __name__ == "__main__":
    asyncio.run(main())