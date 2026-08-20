from config import ROUTING_MODEL, get_settings
from langchain_groq import ChatGroq


def create_supervisor_model():
    """Creates a supervisor model ."""

    model = ChatGroq(
        model=ROUTING_MODEL,
        api_key=get_settings().GROQ_API_KEY,
    )

    return model
