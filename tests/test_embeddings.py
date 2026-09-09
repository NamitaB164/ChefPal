from sentence_transformers import SentenceTransformer

from recommendation_mcp.retrieval.embeddings import RecipeEmbedder

def test_create_embedding():
    model = SentenceTransformer("all-MiniLM-L6-v2")

    text = "chicken recipe with garlic and pork chops"

    embedding = model.encode(text)

    assert embedding is not None
    assert len(embedding) == 384
def test_batch_embedding():
    recipes = [
        {
            "recipe_id": 1,
            "name": "chicken pasta",
            "description": "Simple chicken pasta",
            "ingredients": ["chicken", "pasta"],
            "tags": ["chicken"],
        },
        {
            "recipe_id": 2,
            "name": "chocolate cake",
            "description": "Simple chocolate cake",
            "ingredients": ["flour", "cocoa"],
            "tags": ["dessert"],
        },
    ]

    embedder = RecipeEmbedder()

    embeddings = embedder.embed_batch(recipes, batch_size=2)

    assert len(embeddings) == 2
    assert len(embeddings[0]) == 384
    assert len(embeddings[1]) == 384