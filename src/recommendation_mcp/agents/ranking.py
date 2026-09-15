
from pydantic import BaseModel

from recommendation_mcp.agents.planner import MealRequest
from recommendation_mcp.agents.retrieval import RetrievedRecipe


class RankedRecipe(BaseModel):
    recipe_id: int
    score: float
    reason: str


class RankingResult(BaseModel):
    recommendations: list[RankedRecipe]


class RankingAgent:
    def _deterministic_score(
        self,
        request: MealRequest,
        candidate: RetrievedRecipe,
        min_retrieval: float,
        max_retrieval: float,
        min_rating: float,
        max_rating: float,
        min_protein: float,
        max_protein: float,
    ) -> float:
        retrieval_range = max_retrieval - min_retrieval
        rating_range = max_rating - min_rating
        protein_range = max_protein - min_protein

        retrieval_score = (
            (candidate.score - min_retrieval) / retrieval_range
            if retrieval_range > 0
            else 1.0
        )

        rating_score = (
            (candidate.recipe["rating"] - min_rating) / rating_range
            if rating_range > 0
            else 1.0
        )

        score = 0.7 * retrieval_score + 0.3 * rating_score

        if "high protein" in request.dietary_preferences:
            protein_score = (
                (candidate.recipe["protein_pdv"] - min_protein) / protein_range
                if protein_range > 0
                else 1.0
            )
            score = 0.5 * retrieval_score + 0.2 * rating_score + 0.3 * protein_score

        return score

    def _reason(
        self,
        request: MealRequest,
        candidate: RetrievedRecipe,
    ) -> str:
        recipe = candidate.recipe

        if "high protein" in request.dietary_preferences:
            return (
                f"Strong match for the high-protein preference with "
                f"{recipe['protein_pdv']} protein PDV and a rating of "
                f"{recipe['rating']:.2f}."
            )

        return (
            f"Strong match based on recipe relevance and a rating of "
            f"{recipe['rating']:.2f}."
        )

    async def rank(
        self,
        request: MealRequest,
        candidates: list[RetrievedRecipe],
    ) -> RankingResult:
        if not candidates:
            return RankingResult(recommendations=[])

        retrieval_scores = [candidate.score for candidate in candidates]
        ratings = [candidate.recipe["rating"] for candidate in candidates]
        protein_values = [
            candidate.recipe["protein_pdv"] for candidate in candidates
        ]

        min_retrieval = min(retrieval_scores)
        max_retrieval = max(retrieval_scores)
        min_rating = min(ratings)
        max_rating = max(ratings)
        min_protein = min(protein_values)
        max_protein = max(protein_values)

        scored_candidates = []

        for candidate in candidates:
            score = self._deterministic_score(
                request=request,
                candidate=candidate,
                min_retrieval=min_retrieval,
                max_retrieval=max_retrieval,
                min_rating=min_rating,
                max_rating=max_rating,
                min_protein=min_protein,
                max_protein=max_protein,
            )

            scored_candidates.append((candidate, score))

        scored_candidates.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        recommendations = [
            RankedRecipe(
                recipe_id=candidate.recipe_id,
                score=round(score, 4),
                reason=self._reason(request, candidate),
            )
            for candidate, score in scored_candidates
        ]

        return RankingResult(recommendations=recommendations)

