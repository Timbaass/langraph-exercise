from app_agents.guardrails.trip_guardrail_middleware import TripGuardrailMiddleware
from app_agents.state import TripState

_guardrail = TripGuardrailMiddleware()

async def guardrail_node(state: TripState):
    result = await _guardrail.before_agent(state, None)
    if result is None:
        return {}
    return {"blocked": True, "messages": result["messages"]}