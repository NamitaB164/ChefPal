import pickle
from pathlib import Path

from rank_bm25 import BM25Okapi


class BM25Store:
    def __init__(self) -> None:
        self.bm25: BM25Okapi | None = None
        self.recipe_ids: list[int] = []

    def build_text(self, recipe: dict) -> str:
        return " ".join(
            [
                recipe["name"],
                recipe["description"],
                " ".join(recipe["ingredients"]),
                " ".join(recipe["tags"]),
                " ".join(recipe["steps"]),
            ]
        )

    def build_index(self, recipes: list[dict]) -> None:
        documents = [
            self.build_text(recipe)
            for recipe in recipes
        ]

        tokenized_documents = [
            document.lower().split()
            for document in documents
        ]

        self.bm25 = BM25Okapi(tokenized_documents)
        self.recipe_ids = [
            recipe["recipe_id"]
            for recipe in recipes
        ]

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[tuple[int, float]]:
        if self.bm25 is None:
            raise RuntimeError("BM25 index has not been built.")

        query_tokens = query.lower().split()

        scores = self.bm25.get_scores(query_tokens)

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda index: scores[index],
            reverse=True,
        )[:limit]

        return [
            (self.recipe_ids[index], float(scores[index]))
            for index in ranked_indices
        ]

    def save(self, path: Path) -> None:
        if self.bm25 is None:
            raise RuntimeError("BM25 index has not been built.")

        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("wb") as file:
            pickle.dump(
                {
                    "bm25": self.bm25,
                    "recipe_ids": self.recipe_ids,
                },
                file,
            )

    @classmethod
    def load(cls, path: Path) -> "BM25Store":
        with path.open("rb") as file:
            data = pickle.load(file)

        store = cls()
        store.bm25 = data["bm25"]
        store.recipe_ids = data["recipe_ids"]

        return store