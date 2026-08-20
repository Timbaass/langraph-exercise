from langgraph.graph import StateGraph

from langfuse.langchain import CallbackHandler

FINAL_RESPONSE_NODES = {"trip_node", "flight_node", "clarify_node"}


def create_graph_config(session_thread_id: str, callback_handler: CallbackHandler):
    return {
        "configurable": {"thread_id": session_thread_id},
        "callbacks": [callback_handler],
        "metadata": {
            "langfuse_session_id": session_thread_id,
        },
    }


async def run_graph(
    session_thread_id: str,
    query: str,
    graph: StateGraph,
    callback_handler: CallbackHandler,
):
    """
    Run the LangGraph state graph with the given query and session thread ID.
    """
    config = create_graph_config(session_thread_id, callback_handler)
    result = await graph.ainvoke(
        {"messages": [{"role": "user", "content": query}]}, config=config
    )

    final_output = result["messages"][-1].content
    return final_output


async def stream_graph(
    session_thread_id: str,
    query: str,
    graph: StateGraph,
    callback_handler: CallbackHandler,
):
    """Yield text chunks from the final user-facing agent in the graph."""
    config = create_graph_config(session_thread_id, callback_handler)

    async for message, metadata in graph.astream(
        {"messages": [{"role": "user", "content": query}]},
        config=config,
        stream_mode="messages",
    ):
        if metadata.get("langgraph_node") not in FINAL_RESPONSE_NODES:
            continue

        if getattr(message, "tool_calls", None) or getattr(
            message, "tool_call_chunks", None
        ):
            continue

        if isinstance(message.content, str) and message.content:
            yield message.content
