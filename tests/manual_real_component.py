import asyncio
import time

import recommendation_mcp.agents.planner as planner_module
from recommendation_mcp.agents.planner import PlannerAgent
from recommendation_mcp.agents.retrieval import RetrievalAgent
from recommendation_mcp.agents.ranking import RankingAgent
from recommendation_mcp.mcp_client.client import RecommendationMCPClient
print("PLANNER MODULE:", planner_module.__file__)
print("MEAL REQUEST MODULE:", planner_module.MealRequest.__module__)
print(
    "MEAL REQUEST FIELDS:",
    planner_module.MealRequest.model_fields,
)

query = (
    "I want a high-protein vegetarian dinner with chicken-style savory flavors, under 500 calories, that takes no more than 30 minutes to prepare. It should be low sodium, suitable for a quick weeknight meal, and preferably have a rating above 4.0. Please give me 5 different recipes, with the highest-protein options first."
)

print("=== PLANNER ===")
start = time.perf_counter()
planner = PlannerAgent()
meal_request = planner.plan(query)
print(f"Finished in {time.perf_counter() - start:.2f}s")
print(meal_request)


async def run_retrieval_and_ranking():
    print("\n=== RETRIEVAL ===")
    start = time.perf_counter()
    client = RecommendationMCPClient()
    retrieval_agent = RetrievalAgent(client)
    retrieval_result = await retrieval_agent.retrieve(meal_request)
    print(f"Finished in {time.perf_counter() - start:.2f}s")
    print(retrieval_result)

    print("\n=== RANKING ===")
    start = time.perf_counter()
    ranking_agent = RankingAgent()
    ranking_result = await ranking_agent.rank(
        request=meal_request,
        candidates=retrieval_result.candidates,
    )
    print(f"Finished in {time.perf_counter() - start:.2f}s")
    print(ranking_result)


asyncio.run(run_retrieval_and_ranking())