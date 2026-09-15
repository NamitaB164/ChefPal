from recommendation_mcp.agents.planner import PlannerAgent
from recommendation_mcp.agents.retrieval import RetrievalAgent
from recommendation_mcp.graph.state import RecommendationState
from recommendation_mcp.mcp_client.client import RecommendationMCPClient
from recommendation_mcp.agents.ranking import RankingAgent

def planner_node(state: RecommendationState) -> dict:
    planner = PlannerAgent()

    meal_request = planner.plan(state["user_query"])

    return {
        "meal_request": meal_request,
    }


async def retrieval_node(
    state: RecommendationState,
    mcp_client=None,
) -> dict:
    if mcp_client is None:
        mcp_client = RecommendationMCPClient()

    retrieval_agent = RetrievalAgent(mcp_client)

    retrieval_result = await retrieval_agent.retrieve(
        state["meal_request"]
    )

    return {
        "retrieval_result": retrieval_result,
    }
async def ranking_node(
    state: RecommendationState,
    ranking_agent=None,
) -> dict:
    if ranking_agent is None:
        ranking_agent = RankingAgent()

    ranking_result = await ranking_agent.rank(
        request=state["meal_request"],
        candidates=state["retrieval_result"].candidates,
    )

    return {
        "ranking_result": ranking_result,
    }