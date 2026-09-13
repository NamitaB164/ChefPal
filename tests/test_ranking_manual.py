import asyncio

from recommendation_mcp.agents.planner import MealRequest
from recommendation_mcp.agents.ranking import RankingAgent
from recommendation_mcp.agents.retrieval import RetrievedRecipe


async def main():
    agent = RankingAgent()

    request = MealRequest(
        query="chicken dinner",
        max_calories=500,
        max_minutes=30,
        dietary_preferences=["high protein"],
    )

    candidates = [
        RetrievedRecipe(
            recipe_id=159348,
            score=0.0161,
            recipe={
                "name": "easiest chicken dinner ever",
                "description": "A simple chicken dinner.",
                "minutes": 25,
                "ingredients": ["chicken", "vegetables"],
                "steps": ["Cook chicken.", "Add vegetables."],
                "tags": ["chicken", "dinner"],
                "calories_kcal": 444.5,
                "protein_pdv": 35.0,
                "rating": 4.5,
                "num_ratings": 100,
            },
        ),
        RetrievedRecipe(
            recipe_id=115420,
            score=0.0159,
            recipe={
                "name": "30 minute almond chicken",
                "description": "Chicken with almonds.",
                "minutes": 30,
                "ingredients": ["chicken", "almonds"],
                "steps": ["Cook chicken.", "Add almonds."],
                "tags": ["chicken", "dinner"],
                "calories_kcal": 357.1,
                "protein_pdv": 50.0,
                "rating": 4.7,
                "num_ratings": 200,
            },
        ),
        RetrievedRecipe(
            recipe_id=56704,
            score=0.0154,
            recipe={
                "name": "chicken piccata",
                "description": "Chicken piccata with lemon.",
                "minutes": 20,
                "ingredients": ["chicken", "lemon"],
                "steps": ["Cook chicken.", "Add lemon."],
                "tags": ["chicken", "dinner"],
                "calories_kcal": 280.8,
                "protein_pdv": 20.0,
                "rating": 4.3,
                "num_ratings": 80,
            },
        ),
    ]

    result = await agent.rank(request, candidates)

    print("\nRanked recommendations:")
    for recommendation in result.recommendations:
        print(
            recommendation.recipe_id,
            recommendation.score,
            recommendation.reason,
        )


if __name__ == "__main__":
    asyncio.run(main())