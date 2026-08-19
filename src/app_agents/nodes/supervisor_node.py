# supervisor_node.py
from langchain_core.messages import SystemMessage, HumanMessage
from app_agents.definitions.supervisor_agent import create_supervisor_model
from app_agents.state import TripState, RoutingDecision

supervisor_model = create_supervisor_model()


async def supervisor_node(state: TripState):
    """Normal node — updates state, RETURN VALUE IS ALWAYS A DICT."""
    flight_pending = state.get("flight_status") == "needs_info"

    if flight_pending:
        return {"route": "flight_node"}

    result: RoutingDecision = await supervisor_model.with_structured_output(
        RoutingDecision
    ).ainvoke([
        SystemMessage(
            content="You are a supervisor agent that decides whether to route the "
            "user to the trip agent or the flight agent based on the user's messages. "
            "If the user provides ambiguous or incomplete information, set decision to 'clarify'."
        ),
        *state["messages"],
    ])

    if result.decision == "trip":
        return {"route": "trip_node"}

    if result.decision == "flight":
        return {"route": "flight_node"}

    return {"route": "clarify_node"}


def route_after_supervisor(state: TripState) -> str:
    """Conditional edge function — only reads state, routes. Writes nothing."""
    return state["route"]

async def route_after_guardrail(state):
    if state.get("blocked"):
        return "clarify_node"
    return "supervisor"