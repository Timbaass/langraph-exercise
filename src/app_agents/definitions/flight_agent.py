from langchain.agents import create_agent
from langchain_groq import ChatGroq

from app_agents.tools.flight_tool import create_flight_search_tool
from app_agents.mcp.EnuygunMCP import EnuygunMCP

def create_flight_agent(model: ChatGroq, mcp: EnuygunMCP):
    """Creates a flight agent with the given model."""

    search_flight = create_flight_search_tool(mcp=mcp)

    return create_agent(
        model=model,
        tools=[search_flight],
    )
