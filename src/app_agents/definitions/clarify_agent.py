from config import get_settings
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI


def create_clarify_agent():
    """Creates a clarify agent with the given model."""

    model = ChatOpenAI(
        model="Qwen/Qwen3.5-122B",
        base_url=get_settings().LITELLM_BASE_URL,
        api_key=get_settings().LITELLM_API_KEY
    )

    return create_agent(
        model=model,
        system_prompt="You are a clarify agent that helps users clarify their needs and provide additional information. Use your knowledge and reasoning to ask relevant questions and gather necessary details.",
    )
