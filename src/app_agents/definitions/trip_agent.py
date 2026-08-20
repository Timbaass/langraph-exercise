from langchain.agents import create_agent

from app_agents.tools.weather_tool import get_weather

from config import get_settings
from langchain_openai import ChatOpenAI


def create_trip_agent():
    """Creates a trip agent."""

    model = ChatOpenAI(
        model="Qwen/Qwen3.5-122B",
        base_url=get_settings().LITELLM_BASE_URL,
        api_key=get_settings().LITELLM_API_KEY,
    )

    trip_agent = create_agent(
        model=model,
        tools=[get_weather],
        system_prompt="You are a trip agent that helps users plan trips based on their needs. Use the weather tool if needed to check conditions and provide recommendations.",
    )

    return trip_agent
