import json

from recommendation_mcp.retrieval.embeddings import RecipeEmbedder


def test_recipe_embedding():
    with open("data/processed/recipes.jsonl", encoding="utf-8") as file:
        recipe = json.loads(file.readline())

    embedder = RecipeEmbedder()

    text = embedder.build_text(recipe)
    embedding = embedder.embed(recipe)

    assert "Name:" in text
    assert "Ingredients:" in text
    assert len(embedding) == 384