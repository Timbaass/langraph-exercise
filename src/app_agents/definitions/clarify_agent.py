from config import get_settings
from langchain.agents import create_agent
from langchain_groq import ChatGroq


def create_clarify_agent():
    """Creates a clarify agent with the given model."""

    model = ChatGroq(model="openai/gpt-oss-120b", api_key=get_settings().GROQ_API_KEY)

    return create_agent(
        model=model,
        system_prompt="You are a clarify agent that helps users clarify their needs and provide additional information. Use your knowledge and reasoning to ask relevant questions and gather necessary details.",
    )
