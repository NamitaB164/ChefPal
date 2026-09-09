from recommendation_mcp.retrieval.hybrid import HybridRetriever


def test_hybrid_retrieval():
    retriever = HybridRetriever()

    results = retriever.search(
        "healthy chicken dinner",
        limit=5,
    )

    retriever.close()

    assert len(results) == 5
    assert all(isinstance(recipe_id, int) for recipe_id, _score in results)
    assert all(score > 0 for _recipe_id, score in results)