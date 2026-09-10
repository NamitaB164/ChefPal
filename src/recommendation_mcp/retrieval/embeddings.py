from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"


class RecipeEmbedder:
    def __init__(self) -> None:
        self.model = SentenceTransformer(MODEL_NAME)

    def build_text(self, recipe: dict) -> str:
        return (
            f"Name: {recipe['name']}\n"
            f"Description: {recipe['description']}\n"
            f"Ingredients: {', '.join(recipe['ingredients'])}\n"
            f"Tags: {', '.join(recipe['tags'])}"
        )

    def embed(self, recipe: dict) -> list[float]:
        text = self.build_text(recipe)
        embedding = self.model.encode(text)

        return embedding.tolist()
    def embed_batch(
        self,
        recipes: list[dict],
        batch_size: int = 32,
        ) -> list[list[float]]:
        texts = [self.build_text(recipe) for recipe in recipes]

        embeddings = self.model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        )

        return embeddings.tolist()