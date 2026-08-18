from langchain.agents import create_agent
from langchain_groq import ChatGroq

from app_agents.guardrails.trip_guardrail_middleware import TripGuardrailMiddleware

from config import get_settings


def create_supervisor_model():
    """Creates a supervisor model ."""

    model = ChatGroq(model="openai/gpt-oss-120b", api_key=get_settings().GROQ_API_KEY)

    return  model
