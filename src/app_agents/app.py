import sys
import io

# Force UTF-8 output so non-ASCII characters (Turkish, special hyphens, etc.)
# don't crash on Windows cp1252 consoles.
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.graph import StateGraph, END, START

from app_agents.nodes import trip_node, flight_node, guardrail_node, clarify_node, supervisor_node, route_after_supervisor
from app_agents.nodes.supervisor_node import route_after_guardrail

from app_agents.state import TripState

def build_graph(checkpointer: AsyncPostgresSaver = None):
    graph_builder = StateGraph(TripState)
    graph_builder.add_node("guardrail", guardrail_node)
    graph_builder.add_node("supervisor", supervisor_node)
    graph_builder.add_node("trip_node", trip_node)
    graph_builder.add_node("flight_node", flight_node)
    graph_builder.add_node("clarify_node", clarify_node)

    graph_builder.add_edge(START, "guardrail")
    graph_builder.add_conditional_edges("guardrail", route_after_guardrail)
    graph_builder.add_conditional_edges("supervisor", route_after_supervisor)
    graph_builder.add_edge("trip_node", END)
    graph_builder.add_edge("flight_node", END)
    graph_builder.add_edge("clarify_node", END)

    return graph_builder.compile(checkpointer = checkpointer)