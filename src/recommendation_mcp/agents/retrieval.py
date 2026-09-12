from pydantic import BaseModel, Field

from recommendation_mcp.agents.planner import MealRequest


class RetrievedRecipe(BaseModel):
    recipe_id: int
    score: float
    recipe: dict


class RetrievalResult(BaseModel):
    candidates: list[RetrievedRecipe] = Field(default_factory=list)
    
class RetrievalAgent:
    def __init__(self, mcp_client):
        self.mcp_client = mcp_client

    async def retrieve(self, request: MealRequest) -> RetrievalResult:
        search_results = await self.mcp_client.hybrid_search(
            query=request.query,
            limit=10,
        )

        recipe_ids = [
            item["recipe_id"]
            for item in search_results
        ]

        filtered_ids = await self.mcp_client.filter_recipe_ids(
            recipe_ids=recipe_ids,
            max_calories=request.max_calories,
            max_minutes=request.max_minutes,
        )

        candidates = []

        for item in search_results:
            recipe_id = item["recipe_id"]

            if recipe_id not in filtered_ids:
                continue

            recipe = await self.mcp_client.get_recipe_by_id(recipe_id)

            if recipe is None:
                continue

            candidates.append(
                RetrievedRecipe(
                    recipe_id=recipe_id,
                    score=item["score"],
                    recipe=recipe,
                )
            )

        return RetrievalResult(candidates=candidates)