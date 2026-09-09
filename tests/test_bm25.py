import json
from pathlib import Path
from recommendation_mcp.retrieval.bm25_store import BM25Store


def test_bm25_real_recipe_search():
    recipes = []

    with open("data/processed/recipes.jsonl", encoding="utf-8") as file:
        for index, line in enumerate(file):
            recipes.append(json.loads(line))

            if index == 99:
                break

    store = BM25Store()
    store.build_index(recipes)

    results = store.search("chicken", limit=5)

    assert len(results) == 5
    assert all(isinstance(recipe_id, int) for recipe_id, _ in results)
    assert all(isinstance(score, float) for _, score in results)
def test_bm25_save_and_load(tmp_path: Path):
    recipes = [
        {
            "recipe_id": 1,
            "name": "chicken garlic pasta",
            "description": "A simple chicken pasta dinner",
            "ingredients": ["chicken", "garlic", "pasta"],
            "tags": ["chicken", "pasta"],
            "steps": ["Cook the chicken", "Add garlic and pasta"],
        },
        {
            "recipe_id": 2,
            "name": "chocolate cake",
            "description": "A rich chocolate dessert",
            "ingredients": ["flour", "cocoa", "sugar"],
            "tags": ["dessert", "cake"],
            "steps": ["Mix ingredients", "Bake the cake"],
        },
    ]

    store = BM25Store()
    store.build_index(recipes)

    index_path = tmp_path / "bm25.pkl"
    store.save(index_path)

    loaded_store = BM25Store.load(index_path)

    results = loaded_store.search("chicken pasta", limit=1)

    assert results[0][0] == 1