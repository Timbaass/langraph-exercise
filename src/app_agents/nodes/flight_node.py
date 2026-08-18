from app_agents.definitions.flight_agent import create_flight_agent

from app_agents.state import TripState

flight_agent = create_flight_agent()


async def flight_node(state: TripState):
    """
    Flight node — delegates to the flight planning agent and merges its
    output back into the shared graph state.
    """

    result = await flight_agent.ainvoke({"messages": state["messages"]})


    return {"messages": result["messages"], "flight_status": "complete"}
