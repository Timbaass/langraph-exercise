from langchain_groq import ChatGroq

from config import get_settings


def create_supervisor_model():
    """Creates a supervisor model ."""

    model = ChatGroq(model="openai/gpt-oss-120b", api_key=get_settings().GROQ_API_KEY)

    return  model
