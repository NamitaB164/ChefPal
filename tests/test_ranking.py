from recommendation_mcp.agents.planner import MealRequest
from recommendation_mcp.agents.ranking import RankedRecipe, RankingResult
from recommendation_mcp.agents.retrieval import RetrievedRecipe


def test_ranked_recipe():
    result = RankedRecipe(
        recipe_id=123,
        score=0.95,
        reason="High protein and closely matches the requested meal.",
    )

    assert result.recipe_id == 123
    assert result.score == 0.95
    assert result.reason.startswith("High protein")


def test_ranking_result():
    result = RankingResult(
        recommendations=[
            RankedRecipe(
                recipe_id=123,
                score=0.95,
                reason="Good match.",
            )
        ]
    )

    assert len(result.recommendations) == 1
    assert result.recommendations[0].recipe_id == 123


def test_retrieved_recipe_can_be_ranked():
    request = MealRequest(
        query="chicken dinner",
        dietary_preferences=["high protein"],
    )

    candidate = RetrievedRecipe(
        recipe_id=123,
        score=0.016,
        recipe={
            "name": "High Protein Chicken",
            "calories_kcal": 400,
        },
    )

    assert request.query == "chicken dinner"
    assert candidate.recipe_id == 123
import pytest

from recommendation_mcp.agents.ranking import RankingAgent


def test_ranking_result_rejects_unknown_recipe_id(monkeypatch):
    agent = RankingAgent()

    request = MealRequest(query="chicken dinner")

    candidates = [
        RetrievedRecipe(
            recipe_id=123,
            score=0.9,
            recipe={"name": "Chicken Dinner"},
        )
    ]

    invalid_result = RankingResult(
        recommendations=[
            {
                "recipe_id": 999,
                "score": 1.0,
                "reason": "Invalid candidate.",
            }
        ]
    )

    class FakeResponse:
        message = type(
            "Message",
            (),
            {"content": invalid_result.model_dump_json()},
        )()

    def fake_chat(**kwargs):
        return FakeResponse()

    monkeypatch.setattr("recommendation_mcp.agents.ranking.ollama.chat", fake_chat)

    with pytest.raises(
        ValueError,
        match="Ranking agent returned unknown recipe ID: 999",
    ):
        import asyncio

        asyncio.run(agent.rank(request, candidates))