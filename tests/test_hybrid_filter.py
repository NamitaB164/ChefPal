from recommendation_mcp.retrieval.hybrid import HybridRetriever
from recommendation_mcp.storage.database import (
    filter_recipes,
    get_connection,
)


def test_hybrid_results_can_be_filtered():
    retriever = HybridRetriever()

    results = retriever.search(
        "healthy chicken dinner",
        limit=10,
    )

    recipe_ids = [recipe_id for recipe_id, _score in results]

    connection = get_connection()

    filtered_ids = filter_recipes(
        connection,
        recipe_ids,
        max_calories=500,
    )

    connection.close()
    retriever.close()

    assert len(filtered_ids) <= len(recipe_ids)
    assert all(recipe_id in recipe_ids for recipe_id in filtered_ids)