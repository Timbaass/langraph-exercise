from langchain.agents import create_agent
from langchain_groq import ChatGroq

from app_agents.tools.weather_tool import get_weather
from config import Settings


def create_trip_agent(settings: Settings):
    model = ChatGroq(model="openai/gpt-oss-120b", api_key=settings.GROQ_API_KEY)

    trip_agent = create_agent(
        model=model,
        tools=[get_weather],
    )

    return trip_agent
