from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


class RecommendationMCPClient:
    def __init__(self, server_url: str = "http://127.0.0.1:8000/mcp"):
        self.server_url = server_url

    async def _call_tool(self, tool_name: str, arguments: dict):
        async with streamable_http_client(self.server_url) as (
            read_stream,
            write_stream,
            ):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()

                result = await session.call_tool(
                tool_name,
                arguments=arguments,
                )

                return result.structured_content["result"]

    async def hybrid_search(self, query: str, limit: int = 10):
        return await self._call_tool(
            "hybrid_search",
            {
                "query": query,
                "limit": limit,
            },
        )

    async def filter_recipe_ids(
        self,
        recipe_ids: list[int],
        max_calories: float | None = None,
        max_minutes: int | None = None,
        min_rating: float | None = None,
        required_tags: list[str] | None = None,
    ):
        return await self._call_tool(
            "filter_recipe_ids",
            {
                "recipe_ids": recipe_ids,
                "max_calories": max_calories,
                "max_minutes": max_minutes,
                "min_rating": min_rating,
                "required_tags": required_tags,
            },
        )

    async def get_recipe_by_id(self, recipe_id: int):
        return await self._call_tool(
            "get_recipe_by_id",
            {
                "recipe_id": recipe_id,
            },
        )