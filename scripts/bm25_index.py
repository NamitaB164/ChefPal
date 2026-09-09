import json
from pathlib import Path

from recommendation_mcp.retrieval.bm25_store import BM25Store

INPUT_FILE = Path("data/processed/recipes.jsonl")
OUTPUT_FILE = Path("data/processed/bm25/index.pkl")


def main() -> None:
    recipes = []

    with INPUT_FILE.open(encoding="utf-8") as file:
        for line in file:
            recipes.append(json.loads(line))

    print(f"Loaded {len(recipes)} recipes")

    store = BM25Store()
    store.build_index(recipes)

    store.save(OUTPUT_FILE)

    print(f"BM25 index saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()