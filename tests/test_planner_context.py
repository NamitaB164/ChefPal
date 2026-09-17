from recommendation_mcp.agents.planner import PlannerAgent

print("before")

planner = PlannerAgent()

print("agent created")

result = planner.plan(
    "I want a high protein chicken dinner under "
    "500 calories and ready in 30 minutes"
)

print("after")
print(result)