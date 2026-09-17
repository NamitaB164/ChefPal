import pytest

from recommendation_mcp.agents.planner import MealRequest
from recommendation_mcp.agents.ranking import RankingResult
from recommendation_mcp.agents.retrieval import RetrievedRecipe, RetrievalResult
from recommendation_mcp.graph.nodes import ranking_node, retrieval_node
from recommendation_mcp.graph.workflow import build_graph


class FakeMCPClient:
    async def hybrid_search(self, query, limit=10):
        return [
            {"recipe_id": 123, "score": 0.9},
            {"recipe_id": 456, "score": 0.8},
        ]

    async def filter_recipe_ids(
    self,
    recipe_ids,
    max_calories=None,
    max_minutes=None,
    min_rating=None,
    required_tags=None,
    ):
        return recipe_ids

    async def get_recipe_by_id(self, recipe_id):
        return {
            "recipe_id": recipe_id,
            "name": f"Recipe {recipe_id}",
            "calories_kcal": 400,
            "minutes": 20,
        }


class FakeRankingAgent:
    async def rank(self, request, candidates):
        return RankingResult(
            recommendations=[
                {
                    "recipe_id": candidates[0].recipe_id,
                    "score": 1.0,
                    "reason": "Best match",
                }
            ]
        )


def test_graph_has_planner_node():
    graph = build_graph()

    assert graph is not None


@pytest.mark.anyio
async def test_graph_runs_planner():
    graph = build_graph(
        mcp_client=FakeMCPClient(),
        ranking_agent=FakeRankingAgent(),
    )

    result = await graph.ainvoke(
        {
            "user_query": "chicken dinner under 500 calories",
            "meal_request": None,
            "retrieval_result": None,
            "ranking_result": None,
        }
    )

    assert result["meal_request"] is not None
    assert result["meal_request"].query == "chicken dinner"
    assert result["meal_request"].max_calories == 500

    assert result["retrieval_result"] is not None
    assert len(result["retrieval_result"].candidates) == 2

    assert result["ranking_result"] is not None
    assert len(result["ranking_result"].recommendations) == 1
    assert result["ranking_result"].recommendations[0].recipe_id == 123


@pytest.mark.anyio
async def test_retrieval_node():
    state = {
        "user_query": "chicken dinner",
        "meal_request": MealRequest(
            query="chicken dinner",
            max_calories=500,
        ),
        "retrieval_result": None,
        "ranking_result": None,
    }

    result = await retrieval_node(
        state,
        mcp_client=FakeMCPClient(),
    )

    assert isinstance(result["retrieval_result"], RetrievalResult)
    assert len(result["retrieval_result"].candidates) == 2
    assert result["retrieval_result"].candidates[0].recipe_id == 123


@pytest.mark.anyio
async def test_ranking_node():
    state = {
        "user_query": "high protein chicken dinner",
        "meal_request": MealRequest(
            query="chicken dinner",
            dietary_preferences=["high protein"],
        ),
        "retrieval_result": RetrievalResult(
            candidates=[
                RetrievedRecipe(
                    recipe_id=123,
                    score=0.9,
                    recipe={
                        "recipe_id": 123,
                        "name": "Chicken Dinner",
                        "calories_kcal": 400,
                        "minutes": 20,
                    },
                ),
            ]
        ),
        "ranking_result": None,
    }

    result = await ranking_node(
        state,
        ranking_agent=FakeRankingAgent(),
    )

    assert isinstance(result["ranking_result"], RankingResult)
    assert len(result["ranking_result"].recommendations) == 1
    assert result["ranking_result"].recommendations[0].recipe_id == 123