import asyncio

from recommendation_mcp.mcp_client.client import RecommendationMCPClient


async def main():
    client = RecommendationMCPClient()

    result = await client.hybrid_search("chicken dinner", limit=5)

    print(type(result))
    print(result)


if __name__ == "__main__":
    asyncio.run(main())