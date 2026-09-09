from recommendation_mcp.retrieval.rrf import reciprocal_rank_fusion


def test_rrf_combines_rankings():
    dense = [1, 2, 3]
    sparse = [2, 1, 4]

    results = reciprocal_rank_fusion([dense, sparse])

    assert results[0][0] in {1, 2}
    assert results[1][0] in {1, 2}
    assert results[2][0] in {3, 4}
def test_rrf_calculates_scores_correctly():
    rankings = [
        [1, 2, 3],
        [2, 1, 4],
    ]

    results = reciprocal_rank_fusion(rankings, k=60)

    scores = dict(results)

    expected_recipe_1 = 1 / 61 + 1 / 62
    expected_recipe_2 = 1 / 62 + 1 / 61
    expected_recipe_3 = 1 / 63
    expected_recipe_4 = 1 / 63

    assert scores[1] == expected_recipe_1
    assert scores[2] == expected_recipe_2
    assert scores[3] == expected_recipe_3
    assert scores[4] == expected_recipe_4