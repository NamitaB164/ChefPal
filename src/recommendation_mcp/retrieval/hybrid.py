from pathlib import Path

from recommendation_mcp.retrieval.bm25_store import BM25Store
from recommendation_mcp.retrieval.embeddings import RecipeEmbedder
from recommendation_mcp.retrieval.qdrant_store import get_client, search
from recommendation_mcp.retrieval.rrf import reciprocal_rank_fusion

BM25_INDEX = Path("data/processed/bm25/index.pkl")


class HybridRetriever:
    def __init__(self) -> None:
        self.embedder = RecipeEmbedder()
        self.bm25 = BM25Store.load(BM25_INDEX)
        self.client = get_client()

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[tuple[int, float]]:
        dense_embedding = self.embedder.model.encode(query).tolist()

        dense_results = search(
            self.client,
            dense_embedding,
            limit=limit,
        )

        sparse_results = self.bm25.search(
            query,
            limit=limit,
        )

        dense_ranking = [
            recipe_id
            for recipe_id, _score in dense_results
        ]

        sparse_ranking = [
            recipe_id
            for recipe_id, _score in sparse_results
        ]

        results = reciprocal_rank_fusion(
    [dense_ranking, sparse_ranking]
)

        return results[:limit]

    def close(self) -> None:
        self.client.close()