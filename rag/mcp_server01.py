import sys
import json
import asyncio
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("demo-mcp")


@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="add",
            description="两个数字相加",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "add":
        result = arguments["a"] + arguments["b"]
        return TextContent(type="text", text=str(result))
    return TextContent(type="text", text="Unknown tool")


async def main():
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, asyncio.Event())


if __name__ == "__main__":
    asyncio.run(main())
