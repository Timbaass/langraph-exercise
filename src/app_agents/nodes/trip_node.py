from app_agents.definitions.trip_agent import create_trip_agent
from app_agents.state import TripState

trip_agent = create_trip_agent()


async def trip_node(state: TripState):
    """
    Trip node — delegates to the trip planning agent and merges its
    output back into the shared graph state.
    """
    result = await trip_agent.ainvoke({"messages": state["messages"]})

    return {
        "messages": result["messages"],
        "trip_status": "complete",
    }