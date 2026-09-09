import json

from recommendation_mcp.retrieval.embeddings import RecipeEmbedder
from recommendation_mcp.retrieval.qdrant_store import (
    create_collection,
    get_client,
    insert_recipe_embedding,
    search,
)


def test_qdrant_search():
    with open("data/processed/recipes.jsonl", encoding="utf-8") as file:
        recipe = json.loads(file.readline())

    client = get_client()
    create_collection(client)

    embedder = RecipeEmbedder()
    embedding = embedder.embed(recipe)

    insert_recipe_embedding(client, recipe, embedding)

    results = search(client, embedding, limit=5)

    assert len(results) == 5
    assert results[0][0] == recipe["recipe_id"]

    client.close()