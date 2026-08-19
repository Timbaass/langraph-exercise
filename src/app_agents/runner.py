from langgraph.graph import StateGraph

from langfuse.langchain import CallbackHandler


async def run_graph(session_thread_id: str, query: str, graph: StateGraph, callback_handler: CallbackHandler):
    """
    Run the LangGraph state graph with the given query and session thread ID.
    """
    config = {
        "configurable": {"thread_id": session_thread_id},
        "callbacks": [callback_handler],
        "metadata": {
            "langfuse_session_id": session_thread_id,
        },
    }
    result = await graph.ainvoke(
        {"messages": [{"role": "user", "content": query}]}, config=config
    )

    final_output = result["messages"][-1].content
    return final_output
