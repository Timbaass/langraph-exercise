from langchain.agents import create_agent

from app_agents.tools.weather_tool import get_weather

from config import create_qwen_llm


def create_trip_agent():
    """Creates a trip agent."""

    model = create_qwen_llm()

    trip_agent = create_agent(
        model=model,
        tools=[get_weather],
        system_prompt="You are a trip agent that helps users plan trips based on their needs. Use the weather tool if needed to check conditions and provide recommendations.",
    )

    return trip_agent
