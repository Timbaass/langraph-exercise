from config import get_settings
from langchain_openai import ChatOpenAI


def create_supervisor_model():
    """Creates a supervisor model ."""

    model = ChatOpenAI(
        model="Qwen/Qwen3.5-122B",
        base_url=get_settings().LITELLM_BASE_URL,
        api_key=get_settings().LITELLM_API_KEY,
    )

    return model
