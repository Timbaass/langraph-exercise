from langchain.tools import tool

@tool
def get_weather(location: str) -> str:
    """Get the current weather for a given location."""
    # logic to fetch weather data from an API
    # For demonstration purposes, we'll return a placeholder string
    return f"The current weather in {location} is sunny with a temperature of 25°C."