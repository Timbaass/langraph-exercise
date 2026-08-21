from config import create_qwen_llm


def create_supervisor_model():
    """Creates a supervisor model ."""

    model = create_qwen_llm()

    return model
