from langgraph.graph import StateGraph, END, START, MessagesState

from app_agents.nodes import trip_node, flight_node, supervisor_node, guardrail_node

import asyncio

async def route_after_guardrail(state):
    if state.get("blocked"):
        return END
    return await supervisor_node(state)


graph = StateGraph(MessagesState)
graph.add_node("trip_node", trip_node)
graph.add_node("flight_node", flight_node)
graph.add_node("guardrail", guardrail_node)

graph.add_edge(START, "guardrail")
graph.add_conditional_edges("guardrail", route_after_guardrail)
graph.add_edge("trip_node", END)
graph.add_edge("flight_node", END)

graph = graph.compile()

async def main():
    result = await graph.ainvoke(
        {"messages": [{"role": "user", "content": "Malatya'dan İstanbul'a 20.08.2026 ya bir bilet bul."}]}
    )
    print(result)


if __name__ == "__main__":
    asyncio.run(main())