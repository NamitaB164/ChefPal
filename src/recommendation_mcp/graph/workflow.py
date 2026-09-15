from langgraph.graph import END, START, StateGraph

from recommendation_mcp.agents.ranking import RankingAgent
from recommendation_mcp.agents.retrieval import RetrievalAgent
from recommendation_mcp.graph.nodes import planner_node
from recommendation_mcp.graph.nodes import ranking_node
from recommendation_mcp.graph.state import RecommendationState
from recommendation_mcp.mcp_client.client import RecommendationMCPClient


def make_retrieval_node(mcp_client):
    retrieval_agent = RetrievalAgent(mcp_client)

    async def node(state: RecommendationState) -> dict:
        retrieval_result = await retrieval_agent.retrieve(
            state["meal_request"]
        )

        return {
            "retrieval_result": retrieval_result,
        }

    return node


def make_ranking_node(ranking_agent):
    async def node(state: RecommendationState) -> dict:
        return await ranking_node(
            state,
            ranking_agent=ranking_agent,
        )

    return node


def build_graph(mcp_client=None, ranking_agent=None):
    if mcp_client is None:
        mcp_client = RecommendationMCPClient()

    if ranking_agent is None:
        ranking_agent = RankingAgent()

    graph = StateGraph(RecommendationState)

    graph.add_node("planner", planner_node)
    graph.add_node(
        "retrieval",
        make_retrieval_node(mcp_client),
    )
    graph.add_node(
        "ranking",
        make_ranking_node(ranking_agent),
    )

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "retrieval")
    graph.add_edge("retrieval", "ranking")
    graph.add_edge("ranking", END)

    return graph.compile()