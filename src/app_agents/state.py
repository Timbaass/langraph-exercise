from typing import Annotated, Literal

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


class TripState(TypedDict, total=False):
    """State for the outer trip-planning graph.

    This is NOT an AgentState — it is a plain TypedDict used by
    the StateGraph.  The sub-agents created with `create_agent()`
    have their own internal AgentState; we do not inherit from it.
    """

    messages: Annotated[list[AnyMessage], add_messages]
    decision: Literal["flight", "trip", "clarify"] | None
    blocked: bool | None
    route: str | None


class RoutingDecision(BaseModel):
    decision: Literal["flight", "trip", "clarify"] | None = Field(
        default=None, description="Determines which agent should handle the request."
    )
