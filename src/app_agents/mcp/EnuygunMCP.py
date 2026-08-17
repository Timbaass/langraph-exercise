from langchain_mcp_adapters.client import MultiServerMCPClient

from config import get_settings


class EnuygunMCP:
    def __init__(self):
        self.settings = get_settings()
        self.client = MultiServerMCPClient(
            {"enuygun": {"url": self.settings.ENUYGUN_MCP_URL, "transport": "http"}}
        )
        self.tools = []

    async def load_tools(self):
        if self.tools is None:
            self.tools = await self.client.get_tools()
        return self.tools

    async def list_tools_by_name(self, tool_name: str):
        return [tool for tool in await self.load_tools() if tool.name.startswith(tool_name.lower())]

    async def call_tool(self, tool_name: str, input_data: dict):
        tool = next(
            (tool for tool in await self.load_tools() if tool.name.startswith(tool_name.lower())),
            None,
        )
        if not tool:
            raise ValueError(f"Tool '{tool_name}' not found.")
        return await tool.ainvoke(input_data)
