from langgraph.graph import StateGraph, END, START, MessagesState
from app_agents.definitions.trip_agent import create_trip_agent
from config import get_settings

settings = get_settings()

trip_agent = create_trip_agent(settings=settings)


graph = StateGraph(MessagesState)
graph.add_node("trip_agent", trip_agent)

graph.add_edge(START, "trip_agent")
graph.add_edge("trip_agent", END)
graph = graph.compile()

result = graph.invoke({"messages": [{"role": "user", "content": "Hi!"}]})

print(result)