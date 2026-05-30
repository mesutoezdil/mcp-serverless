import asyncio
import os
import requests
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

NEBIUS_ENDPOINT = os.getenv("NEBIUS_ENDPOINT", "http://localhost:8000")

app = Server("nebius-mcp-bridge")

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="embed_text",
            description="Generate embeddings via Nebius Serverless Endpoint (Token Factory)",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to embed"}
                },
                "required": ["text"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "embed_text":
        response = requests.post(
            f"{NEBIUS_ENDPOINT}/call",
            json={"tool": "embed_text", "parameters": arguments}
        )
        result = response.json()
        return [types.TextContent(type="text", text=str(result))]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read, write):
        await app.run(read, write, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
