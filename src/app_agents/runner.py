from app_agents.app import graph


async def run_graph(session_thread_id: str, query: str):
    """
    Run the LangGraph state graph with the given query and session thread ID.
    """
    config = ({"configurable": {"thread_id": session_thread_id}},)

    result = await graph.ainvoke(
        {"messages": [{"role": "user", "content": query}]},
    )

    final_output = result["messages"][-1].content
    return final_output
