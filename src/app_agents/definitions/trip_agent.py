from langchain.agents import create_agent

from app_agents.tools.weather_tool import get_weather

from config import GROQ_MODEL, get_settings
from langchain_groq import ChatGroq


def create_trip_agent():
    """Creates a trip agent."""

    model = ChatGroq(
        model=GROQ_MODEL,
        api_key=get_settings().GROQ_API_KEY,
    )

    trip_agent = create_agent(
        model=model,
        tools=[get_weather],
        system_prompt="You are a trip agent that helps users plan trips based on their needs. Use the weather tool if needed to check conditions and provide recommendations.",
    )

    return trip_agent
