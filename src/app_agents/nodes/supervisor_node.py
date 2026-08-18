from langchain.messages import SystemMessage
from langgraph.types import Send

from app_agents.definitions.supervisor_agent import create_supervisor_model
from app_agents.state import TripState, RoutingDecision

supervisor_model = create_supervisor_model()


async def supervisor_node(state: TripState):

    decision: RoutingDecision = await supervisor_model.with_structured_output(
        RoutingDecision
    ).ainvoke(
        [
            SystemMessage(
                content="You are a supervisor agent that decides whether to route the user to the trip agent or the flight agent based on the user's messages."
            ),
            state["messages"][-1],
        ]
    )

    sends = []

    if decision.needs_trip:
        sends.append(Send("trip_node", {**state, "needs_trip": True}))

    if decision.needs_flight:
        sends.append(Send("flight_node", {**state, "needs_flight": True}))

    return sends
