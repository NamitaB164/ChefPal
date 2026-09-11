from recommendation_mcp.agents.planner import MealRequest, PlannerAgent


def test_meal_request():
    request = MealRequest(
        query="chicken dinner",
        max_calories=500,
        max_minutes=30,
        required_tags=["chicken"],
        dietary_preferences=["high protein"],
    )

    assert request.query == "chicken dinner"
    assert request.max_calories == 500
    assert request.max_minutes == 30
    assert request.required_tags == ["chicken"]
    assert request.dietary_preferences == ["high protein"]
def test_planner_agent():
    planner = PlannerAgent()

    result = planner.plan("chicken dinner")

    assert isinstance(result, MealRequest)
    assert result.query == "chicken dinner"
def test_planner_agent():
    planner = PlannerAgent()

    result = planner.plan(
        "chicken dinner under 500 calories that takes less than 30 minutes"
    )

    assert isinstance(result, MealRequest)
    assert result.query == "chicken dinner"
    assert result.max_calories == 500
    assert result.max_minutes == 30