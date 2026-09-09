from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

QDRANT_PATH = Path("data/qdrant")
COLLECTION_NAME = "recipes"
VECTOR_SIZE = 384


def get_client() -> QdrantClient:
    QDRANT_PATH.mkdir(parents=True, exist_ok=True)

    return QdrantClient(path=str(QDRANT_PATH))


def create_collection(client: QdrantClient) -> None:
    collections = client.get_collections().collections

    if COLLECTION_NAME not in [collection.name for collection in collections]:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )
def insert_recipe_embedding(
    client: QdrantClient,
    recipe: dict,
    embedding: list[float],
) -> None:
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=recipe["recipe_id"],
                vector=embedding,
                payload={
                    "recipe_id": recipe["recipe_id"],
                    "name": recipe["name"],
                    "tags": recipe["tags"],
                    "minutes": recipe["minutes"],
                    "calories_kcal": recipe["nutrition"]["calories_kcal"],
                    "rating": recipe["rating"],
                },
            )
        ],
    )
def search(
    client: QdrantClient,
    query_embedding: list[float],
    limit: int = 5,
) -> list[tuple[int, float]]:
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=limit,
    ).points

    return [
        (int(point.id), float(point.score))
        for point in results
    ]
def insert_recipe_embeddings(
    client: QdrantClient,
    recipes: list[dict],
    embeddings: list[list[float]],
) -> None:
    points = []

    for recipe, embedding in zip(recipes, embeddings):
        points.append(
            PointStruct(
                id=recipe["recipe_id"],
                vector=embedding,
                payload={
                    "recipe_id": recipe["recipe_id"],
                    "name": recipe["name"],
                    "tags": recipe["tags"],
                    "minutes": recipe["minutes"],
                    "calories_kcal": recipe["nutrition"]["calories_kcal"],
                    "rating": recipe["rating"],
                },
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )