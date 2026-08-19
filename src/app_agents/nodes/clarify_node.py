from app_agents.state import TripState
from app_agents.definitions.clarify_agent import create_clarify_agent
from langchain_core.messages import HumanMessage

clarify_agent = create_clarify_agent()


async def clarify_node(state: TripState):
    """
    Clarify node — delegates to the clarify agent and merges its
    output back into the shared graph state.
    """
    # Pass the entire conversation history to the clarify agent
    result = await clarify_agent.ainvoke({"messages": state["messages"]})
    new_messages = result["messages"][len(state["messages"]) :]

    return {"messages": new_messages}
