from langchain.agents import create_agent
from langchain_groq import ChatGroq

from app_agents.tools.flight_tool import create_flight_search_tool
from app_agents.mcp_tools.EnuygunMCP import EnuygunMCP

from config import get_settings


def create_flight_agent():
    """Creates a flight agent with the given model."""

    mcp = EnuygunMCP()
    model = ChatGroq(model="openai/gpt-oss-120b", api_key=get_settings().GROQ_API_KEY)

    search_flight = create_flight_search_tool(mcp=mcp)

    return create_agent(
        model=model,
        tools=[search_flight],
        system_prompt="You are a flight agent that helps users find flights based on their needs. Use the flight search tool to find flights and provide the user with the best options.",
    )
