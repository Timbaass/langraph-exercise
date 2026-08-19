from langchain_core.messages import HumanMessage

from app_agents.definitions.flight_agent import create_flight_agent
from app_agents.state import TripState

flight_agent = create_flight_agent()


async def flight_node(state: TripState):
    """
    Flight node — delegates to the flight planning agent and merges its
    output back into the shared graph state.
    """
    # Pass the entire conversation history to the sub-agent so it remembers context
    # (like origin, destination) when asking for follow-up details (like dates).
    result = await flight_agent.ainvoke({"messages": state["messages"]})

    # The sub-agent returns the full history including new messages; we only want to append the new ones.
    new_messages = result["messages"][len(state["messages"]) :]

    return {
        "messages": new_messages,
    }
