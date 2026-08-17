from langchain.agents import create_agent

from app_agents.tools.weather_tool import get_weather
from app_agents.guardrails.trip_guardrail_middleware import TripGuardrailMiddleware

from langchain_groq import ChatGroq


def create_trip_agent(model: ChatGroq):

    trip_agent = create_agent(
        model=model,
        tools=[get_weather],
        middleware=[TripGuardrailMiddleware()],
    )

    return trip_agent
