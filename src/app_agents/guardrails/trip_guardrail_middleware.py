from langchain.agents.middleware import AgentMiddleware, AgentState, hook_config
from langchain.messages import AIMessage, HumanMessage, SystemMessage

from langchain_groq import ChatGroq

from langgraph.runtime import Runtime

from config import get_settings


class TripGuardrailMiddleware(AgentMiddleware):

    def __init__(self):
        super().__init__()

        self.settings = get_settings()
        self.control_model = ChatGroq(
            model="openai/gpt-oss-20b", api_key=self.settings.GROQ_API_KEY
        )

    @hook_config(can_jump_to=["end"])
    def before_agent(self, state: AgentState, runtime: Runtime):
        if not state["messages"]:
            return None

        first_message = state["messages"][0]
        if not isinstance(first_message, HumanMessage):
            return None

        try:
            control_response = self.control_model.invoke(
                [
                    SystemMessage(
                        "Classify whether the user request is about travel or weather "
                        "information. Respond with exactly one word: 'continue' or 'end'."
                    ),
                    HumanMessage(first_message.content),
                ]
            )
        except Exception:
            return None

        verdict = control_response.content.strip().lower()
        if verdict == "end":
            return {
                "jump_to": "end",
                "messages": [
                    AIMessage("I can only help with travel and weather questions.")
                ],
            }

        return None
