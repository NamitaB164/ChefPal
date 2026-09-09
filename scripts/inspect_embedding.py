from recommendation_mcp.retrieval.qdrant_store import (
    COLLECTION_NAME,
    get_client,
)


def main() -> None:
    client = get_client()

    result = client.retrieve(
        collection_name=COLLECTION_NAME,
        ids=[63986],
        with_payload=True,
        with_vectors=True,
    )

    point = result[0]

    print("Recipe ID:", point.id)
    print("Payload:")
    print(point.payload)

    print("\nVector:")
    print(point.vector)

    print("\nVector dimensions:", len(point.vector))

    client.close()


if __name__ == "__main__":
    main()