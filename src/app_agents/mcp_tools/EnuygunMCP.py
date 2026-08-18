from langchain_mcp_adapters.client import MultiServerMCPClient


class EnuygunMCP:
    def __init__(self):
        self.client = MultiServerMCPClient(
            {"enuygun": {"url": "https://mcp.enuygun.com/mcp", "transport": "http"}}
        )
        self.tools = None

    async def load_tools(self):
        if self.tools is None:
            self.tools = await self.client.get_tools()
        return self.tools

    async def list_tools_by_name(self, tool_name: str):
        return [t for t in await self.load_tools() if t.name.startswith(tool_name.lower())]

    async def call_tool(self, tool_name: str, input_data: dict):
        tool = next(
            (t for t in await self.load_tools() if t.name.startswith(tool_name.lower())),
            None,
        )
        if not tool:
            raise ValueError(f"Tool '{tool_name}' not found.")
        return await tool.ainvoke(input_data)