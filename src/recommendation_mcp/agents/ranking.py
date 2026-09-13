import json

import ollama
from pydantic import BaseModel, Field

from recommendation_mcp.agents.planner import MealRequest
from recommendation_mcp.agents.retrieval import RetrievedRecipe


class RankedRecipe(BaseModel):
    recipe_id: int
    score: float
    reason: str


class RankingResult(BaseModel):
    recommendations: list[RankedRecipe] = Field(default_factory=list)

SYSTEM_PROMPT = """
You are a meal recommendation ranking agent.

Your task is to rank the provided recipe candidates according to the
user's meal request.

Rules:
- Rank only the provided candidates.
- Do not invent recipes or recipe IDs.
- Do not modify or invent recipe data.

Hard constraints:
- All hard constraints such as maximum calories and maximum preparation
  time have already been enforced by the retrieval system.
- Assume every provided candidate satisfies those hard constraints.
- Never claim that a provided candidate violates max_calories or
  max_minutes.
- Do not independently re-rank, reinterpret, or reject candidates based
  on hard constraints.

Ranking:
- Prioritize the user's explicitly stated dietary preferences and meal
  requirements.
- Use recipe relevance, ingredients, tags, nutrition, rating, preparation
  time, and other available recipe information when appropriate.
- Do not treat dataset tags as authoritative dietary certifications.
- Do not infer dietary preferences that the user did not state.
- Qualitative preferences such as "high protein" do not have a fixed
  numeric threshold unless the user explicitly provides one.
- Use relative comparison among candidates rather than claiming that a
  candidate objectively satisfies or fails an undefined qualitative
  preference.
- Do not invent ranking criteria that are not relevant to the user's request.
- A maximum constraint is a limit, not a target. Do not prefer candidates
  for being closer to the maximum allowed value.
- Do not describe a constraint as "required" unless the user explicitly
  stated it as a requirement.
- When comparing protein_pdv, describe it as "protein Daily Value" or
  "protein PDV", never "protein percentage".
- Give each recommendation a concise reason explaining why it is a good
  match for the user's request.

Nutrition:
- protein_pdv, total_fat_pdv, sugar_pdv, sodium_pdv,
  saturated_fat_pdv, and carbs_pdv are percentages of Daily Value (PDV).
- These fields are NOT grams and NOT the percentage of the recipe
  consisting of that nutrient.
- calories_kcal is measured in kcal.
- When referring to a PDV field in a reason, use "Daily Value" or "PDV",
  not "%" unless the context clearly states it is Daily Value percentage.

Output:
- Return the candidates in descending order of recommendation quality.
- The score should be a relative ranking score where a higher score means
  a better recommendation.
- Return only recipes that were provided as candidates.
"""
class RankingAgent:
    def __init__(self, model: str = "qwen2.5:3b"):
        self.model = model

    async def rank(
        self,
        request: MealRequest,
        candidates: list[RetrievedRecipe],
    ) -> RankingResult:
        candidate_data = [
            {
                "recipe_id": candidate.recipe_id,
                "retrieval_score": candidate.score,
                "recipe": candidate.recipe,
            }
            for candidate in candidates
        ]

        prompt = f"""
User request:
{request.model_dump_json(indent=2)}

Candidate recipes:
{json.dumps(candidate_data, ensure_ascii=False, indent=2)}

Rank these candidates for the user.
"""

        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            format=RankingResult.model_json_schema(),
        )

        result = RankingResult.model_validate_json(response.message.content)

        candidate_ids = {candidate.recipe_id for candidate in candidates}

        for recommendation in result.recommendations:
            if recommendation.recipe_id not in candidate_ids:
                raise ValueError(
                    f"Ranking agent returned unknown recipe ID: "
                    f"{recommendation.recipe_id}"
                )

        return result