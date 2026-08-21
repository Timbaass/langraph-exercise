from config import create_qwen_llm
from langchain.agents import create_agent


def create_clarify_agent():
    """Creates a clarify agent with the given model."""

    model = create_qwen_llm()

    return create_agent(
        model=model,
        system_prompt="You are a clarify agent that helps users clarify their needs and provide additional information. Use your knowledge and reasoning to ask relevant questions and gather necessary details.",
    )
