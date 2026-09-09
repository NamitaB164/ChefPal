from recommendation_mcp.retrieval.qdrant_store import (
    COLLECTION_NAME,
    create_collection,
    get_client,
)


def test_create_qdrant_collection():
    client = get_client()
    create_collection(client)

    collections = client.get_collections().collections
    collection_names = [collection.name for collection in collections]

    assert COLLECTION_NAME in collection_names

    client.close()
