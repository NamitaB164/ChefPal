import json

from recommendation_mcp.retrieval.embeddings import RecipeEmbedder
from recommendation_mcp.retrieval.qdrant_store import (
    create_collection,
    get_client,
    insert_recipe_embeddings,
)


def test_qdrant_batch_insert():
    with open("data/processed/recipes.jsonl", encoding="utf-8") as file:
        recipes = [json.loads(file.readline()) for _ in range(2)]

    embedder = RecipeEmbedder()
    embeddings = embedder.embed_batch(recipes, batch_size=2)

    client = get_client()
    create_collection(client)

    insert_recipe_embeddings(client, recipes, embeddings)

    points = client.retrieve(
        collection_name="recipes",
        ids=[recipe["recipe_id"] for recipe in recipes],
    )

    assert len(points) == 2