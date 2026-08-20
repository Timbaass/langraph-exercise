from langchain.agents.middleware import AgentMiddleware, AgentState, hook_config
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from config import get_settings
from langchain_openai import ChatOpenAI


class TripGuardrailMiddleware(AgentMiddleware):

    def __init__(self):
        super().__init__()

        self.settings = get_settings()
        self.control_model = ChatOpenAI(
            model="Qwen/Qwen3.5-122B",
            base_url=get_settings().LITELLM_BASE_URL,
            api_key=get_settings().LITELLM_API_KEY,
        )

    @hook_config(can_jump_to=["end"])
    async def before_agent(self, state: AgentState, runtime):
        if not state["messages"]:
            return None

        last_human_message = next(
            (m for m in reversed(state["messages"]) if isinstance(m, HumanMessage)),
            None,
        )
        if last_human_message is None:
            return None

        try:
            control_response = await self.control_model.ainvoke(
                [
                    SystemMessage(
                        "Classify whether the user request is about travel or weather "
                        "information. Respond with exactly one word: 'continue' or 'end'."
                    ),
                    HumanMessage(last_human_message.content),
                ]
            )
        except Exception:
            return None

        verdict = control_response.content.strip().lower()
        if verdict == "end":
            return {
                "jump_to": "end",
                "messages": [
                    AIMessage("I can only help with trip and flight questions.")
                ],
            }

        return None
