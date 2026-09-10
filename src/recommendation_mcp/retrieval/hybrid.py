
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

    def semantic_search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[tuple[int, float]]:
        query_embedding = self.embedder.model.encode(query).tolist()

        return search(
            self.client,
            query_embedding,
            limit=limit,
        )

    def keyword_search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[tuple[int, float]]:
        return self.bm25.search(
            query,
            limit=limit,
        )

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[tuple[int, float]]:
        dense_results = self.semantic_search(
            query,
            limit=limit,
        )

        sparse_results = self.keyword_search(
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

