from langchain_core.messages import HumanMessage

from app_agents.definitions.trip_agent import create_trip_agent
from app_agents.state import TripState

trip_agent = create_trip_agent()


async def trip_node(state: TripState):
    """
    Trip node — delegates to the trip planning agent and merges its
    output back into the shared graph state.
    """
    # Pass the entire conversation history to the sub-agent
    result = await trip_agent.ainvoke({"messages": state["messages"]})

    # The sub-agent returns the full history including new messages; we only want to append the new ones.
    new_messages = result["messages"][len(state["messages"]) :]

    return {
        "messages": new_messages,
    }
