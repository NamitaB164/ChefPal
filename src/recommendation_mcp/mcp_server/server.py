import json

from mcp.server import MCPServer

from recommendation_mcp.storage.database import (
    filter_recipes,
    get_connection,
    get_recipe,
)

mcp = MCPServer("Recommendation MCP Server")

_hybrid_retriever = None


def get_hybrid_retriever():
    global _hybrid_retriever

    if _hybrid_retriever is None:
        from recommendation_mcp.retrieval.hybrid import HybridRetriever

        _hybrid_retriever = HybridRetriever()

    return _hybrid_retriever

@mcp.tool()
def health_check() -> str:
    """Check whether the Recommendation MCP server is running."""
    return "Recommendation MCP server is healthy."


@mcp.tool()
def get_recipe_by_id(recipe_id: int) -> dict | None:
    """Get a recipe and its nutrition data by recipe ID."""
    connection = get_connection()

    try:
        recipe = get_recipe(connection, recipe_id)

        if recipe is None:
            return None

        result = dict(recipe)

        result["ingredients"] = json.loads(result["ingredients"])
        result["steps"] = json.loads(result["steps"])
        result["tags"] = json.loads(result["tags"])

        return result
    finally:
        connection.close()
@mcp.tool()
def filter_recipe_ids(
    recipe_ids: list[int],
    max_calories: float | None = None,
    max_minutes: int | None = None,
    required_tags: list[str] | None = None,
) -> list[int]:
    """Filter recipe IDs using hard nutrition, time, and tag constraints."""
    connection = get_connection()

    try:
        return filter_recipes(
            connection,
            recipe_ids,
            max_calories=max_calories,
            max_minutes=max_minutes,
            required_tags=required_tags,
        )
    finally:
        connection.close()
@mcp.tool()
def semantic_search(
    query: str,
    limit: int = 5,
) -> list[dict]:
    """Find recipes using semantic similarity search."""
    results = get_hybrid_retriever().semantic_search(
        query,
        limit=limit,
    )

    return [
        {
            "recipe_id": recipe_id,
            "score": score,
        }
        for recipe_id, score in results
    ]

@mcp.tool()
def keyword_search(
    query: str,
    limit: int = 5,
) -> list[dict]:
    """Find recipes using keyword-based BM25 search."""
    results = get_hybrid_retriever().keyword_search(
        query,
        limit=limit,
    )

    return [
        {
            "recipe_id": recipe_id,
            "score": score,
        }
        for recipe_id, score in results
    ]
@mcp.tool()
def hybrid_search(
    query: str,
    limit: int = 5,
) -> list[dict]:
    """Find recipes using hybrid semantic and keyword retrieval."""
    results = get_hybrid_retriever().search(
        query,
        limit=limit,
    )

    return [
        {
            "recipe_id": recipe_id,
            "score": score,
        }
        for recipe_id, score in results
    ]
if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8000,
    )