import json

from recommendation_mcp.retrieval.embeddings import RecipeEmbedder
from recommendation_mcp.retrieval.qdrant_store import (
    COLLECTION_NAME,
    create_collection,
    get_client,
    insert_recipe_embedding,
)


def test_insert_recipe_embedding():
    with open("data/processed/recipes.jsonl", encoding="utf-8") as file:
        recipe = json.loads(file.readline())

    client = get_client()
    create_collection(client)

    embedder = RecipeEmbedder()
    embedding = embedder.embed(recipe)

    insert_recipe_embedding(client, recipe, embedding)

    result = client.retrieve(
        collection_name=COLLECTION_NAME,
        ids=[recipe["recipe_id"]],
        with_payload=True,
    )

    client.close()

    assert len(result) == 1
    assert result[0].payload["recipe_id"] == recipe["recipe_id"]
    assert result[0].payload["name"] == recipe["name"]
