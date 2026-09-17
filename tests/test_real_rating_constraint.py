import pytest

from recommendation_mcp.agents.planner import MealRequest
from recommendation_mcp.agents.retrieval import RetrievalAgent
from recommendation_mcp.mcp_client.client import RecommendationMCPClient


@pytest.mark.anyio
async def test_real_min_rating_constraint():
    client = RecommendationMCPClient("http://127.0.0.1:8000/mcp")
    agent = RetrievalAgent(client)

    request = MealRequest(
        query="chicken dinner",
        max_calories=500,
        min_rating=4.0,
    )

    result = await agent.retrieve(request)

    assert result.candidates

    for candidate in result.candidates:
        recipe = candidate.recipe

        assert recipe["calories_kcal"] <= 500
        assert recipe["rating"] >= 4.0

