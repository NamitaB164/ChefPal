import pytest

from recommendation_mcp.agents.planner import MealRequest
from recommendation_mcp.agents.retrieval import RetrievalAgent


class FakeMCPClient:
    async def hybrid_search(self, query, limit):
        assert query == "chicken dinner"
        assert limit == 50

        return [
            {"recipe_id": 101, "score": 0.9},
            {"recipe_id": 102, "score": 0.8},
            {"recipe_id": 103, "score": 0.7},
        ]

    async def filter_recipe_ids(
        self,
        recipe_ids,
        max_calories=None,
        max_minutes=None,
        min_rating=None,
        required_tags=None,
    ):
        assert recipe_ids == [101, 102, 103]
        assert max_calories == 500
        assert max_minutes == 30
        assert min_rating is None

        return [101, 103]

    async def get_recipe_by_id(self, recipe_id):
        recipes = {
            101: {"name": "Chicken Curry"},
            103: {"name": "Grilled Chicken"},
        }

        return recipes.get(recipe_id)


@pytest.mark.anyio
async def test_retrieval_agent():
    client = FakeMCPClient()
    agent = RetrievalAgent(client)

    request = MealRequest(
        query="chicken dinner",
        max_calories=500,
        max_minutes=30,
    )

    result = await agent.retrieve(request)

    assert len(result.candidates) == 2

    assert result.candidates[0].recipe_id == 101
    assert result.candidates[0].score == 0.9
    assert result.candidates[0].recipe["name"] == "Chicken Curry"

    assert result.candidates[1].recipe_id == 103
    assert result.candidates[1].score == 0.7