from recommendation_mcp.graph.state import RecommendationState


def test_recommendation_state():
    state: RecommendationState = {
        "user_query": "chicken dinner",
        "meal_request": None,
        "retrieval_result": None,
        "ranking_result": None,
    }

    assert state["user_query"] == "chicken dinner"
    assert state["meal_request"] is None
    assert state["retrieval_result"] is None
    assert state["ranking_result"] is None
from recommendation_mcp.graph.nodes import planner_node


def test_planner_node():
    state = {
        "user_query": "chicken dinner under 500 calories",
        "meal_request": None,
        "retrieval_result": None,
        "ranking_result": None,
    }

    result = planner_node(state)

    assert result["meal_request"].query == "chicken dinner"
    assert result["meal_request"].max_calories == 500