import json
from pathlib import Path

from recommendation_mcp.retrieval.embeddings import RecipeEmbedder
from recommendation_mcp.retrieval.qdrant_store import (
    create_collection,
    get_client,
    insert_recipe_embeddings,
)

INPUT_FILE = Path("data/processed/recipes.jsonl")
BATCH_SIZE = 32


def main() -> None:
    recipes = []

    with INPUT_FILE.open(encoding="utf-8") as file:
        for line in file:
            recipes.append(json.loads(line))

    print(f"Loaded {len(recipes)} recipes")

    client = get_client()
    create_collection(client)

    embedder = RecipeEmbedder()

    total = len(recipes)

    for start in range(0, total, BATCH_SIZE):
        batch = recipes[start : start + BATCH_SIZE]

        embeddings = embedder.embed_batch(
            batch,
            batch_size=BATCH_SIZE,
        )

        insert_recipe_embeddings(
            client,
            batch,
            embeddings,
        )

        processed = min(start + BATCH_SIZE, total)
        print(f"Indexed {processed} / {total}")

    print("Finished building Qdrant index")


if __name__ == "__main__":
    main()