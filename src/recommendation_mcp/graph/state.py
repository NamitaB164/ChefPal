from typing import TypedDict

from recommendation_mcp.agents.planner import MealRequest
from recommendation_mcp.agents.ranking import RankingResult
from recommendation_mcp.agents.retrieval import RetrievalResult


class RecommendationState(TypedDict):
    user_query: str
    meal_request: MealRequest | None
    retrieval_result: RetrievalResult | None
    ranking_result: RankingResult | None