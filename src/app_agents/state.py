from typing import Annotated

from langchain.agents import AgentState
from langchain.messages import AnyMessage

from langgraph.graph import add_messages

from pydantic import BaseModel

    
class TripState(AgentState):
    needs_flight: bool | None = None
    needs_trip: bool | None = None
    flight_status: str | None = None
    trip_status: str | None = None
    blocked: bool | None = None
    messages: Annotated[list[AnyMessage], add_messages]


class RoutingDecision(BaseModel):
    needs_trip: bool
    needs_flight: bool