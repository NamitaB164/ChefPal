import asyncio
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


def test_ranking_orders_candidates_by_score():
    agent = RankingAgent()

    request = MealRequest(
        query="chicken dinner",
        dietary_preferences=["high protein"],
    )

    candidates = [
        RetrievedRecipe(
            recipe_id=159348,
            score=0.0161,
            recipe={
                "name": "easiest chicken dinner ever",
                "rating": 4.5,
                "protein_pdv": 35.0,
            },
        ),
        RetrievedRecipe(
            recipe_id=115420,
            score=0.0159,
            recipe={
                "name": "30 minute almond chicken",
                "rating": 4.7,
                "protein_pdv": 50.0,
            },
        ),
        RetrievedRecipe(
            recipe_id=56704,
            score=0.0154,
            recipe={
                "name": "chicken piccata",
                "rating": 4.3,
                "protein_pdv": 20.0,
            },
        ),
    ]

    result = asyncio.run(agent.rank(request, candidates))

    ranked_ids = [
        recommendation.recipe_id
        for recommendation in result.recommendations
    ]

    assert ranked_ids == [115420, 159348, 56704]