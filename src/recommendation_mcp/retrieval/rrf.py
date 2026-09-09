from collections import defaultdict


def reciprocal_rank_fusion(
    rankings: list[list[int]],
    k: int = 60,
) -> list[tuple[int, float]]:
    scores: dict[int, float] = defaultdict(float)

    for ranking in rankings:
        for rank, recipe_id in enumerate(ranking, start=1):
            scores[recipe_id] += 1 / (k + rank)

    return sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True,
    )